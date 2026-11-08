const API_URL =
    "https://effective-engine-r449rjgpjpwwcxq99-7860.app.github.dev/predict_batch";

const analyzeButton = document.getElementById("analyzeButton");
const themeButton = document.getElementById("themeButton");
const copyButton = document.getElementById("copyButton");

const pageStatus = document.getElementById("pageStatus");
const loadingStatus = document.getElementById("loadingStatus");
const resultsContainer = document.getElementById("resultsContainer");
const sentimentFilter = document.getElementById("sentimentFilter");

let allPredictions = [];

// --------------------------------------------------
// 1. Afficher les statistiques retournees par l'API
// --------------------------------------------------

function displayStatistics(data) {

    document.getElementById("totalComments").textContent =
        `Commentaires analysés : ${data.total_comments}`;

    const statistics = data.statistics;

    document.getElementById("negativeCount").textContent =
        statistics.Negatif.count;

    document.getElementById("negativePercentage").textContent =
        `${statistics.Negatif.percentage} %`;

    document.getElementById("neutralCount").textContent =
        statistics.Neutre.count;

    document.getElementById("neutralPercentage").textContent =
        `${statistics.Neutre.percentage} %`;

    document.getElementById("positiveCount").textContent =
        statistics.Positif.count;

    document.getElementById("positivePercentage").textContent =
        `${statistics.Positif.percentage} %`;
}


// --------------------------------------------------
// 2. Afficher les predictions dans l'interface
// --------------------------------------------------

function displayResults() {

    const selectedSentiment = sentimentFilter.value;

    const filteredPredictions = allPredictions.filter(
        prediction =>
            selectedSentiment === "all" ||
            prediction.label === selectedSentiment
    );

    resultsContainer.replaceChildren();

    if (filteredPredictions.length === 0) {

        const message = document.createElement("p");
        message.className = "empty-message";
        message.textContent = "Aucun résultat à afficher.";

        resultsContainer.appendChild(message);
        return;
    }

    filteredPredictions.forEach(prediction => {

        const card = document.createElement("div");
        card.className = `result-card ${prediction.label}`;

        const label = document.createElement("div");
        label.className = "result-label";
        label.textContent = prediction.label;

        const comment = document.createElement("div");
        comment.className = "result-comment";
        comment.textContent = prediction.comment;

        const confidence = document.createElement("div");
        confidence.className = "result-confidence";
        confidence.textContent =
            `Confiance : ${(prediction.confidence * 100).toFixed(2)} %`;

        card.appendChild(label);
        card.appendChild(comment);
        card.appendChild(confidence);

        resultsContainer.appendChild(card);
    });
}


// --------------------------------------------------
// 3. Recuperer les commentaires depuis YouTube
// --------------------------------------------------

async function extractYouTubeComments() {

    const tabs = await chrome.tabs.query({
        active: true,
        currentWindow: true
    });

    const activeTab = tabs[0];

    if (
        !activeTab ||
        !activeTab.url ||
        !/^https:\/\/(www\.youtube\.com|m\.youtube\.com)\//.test(activeTab.url)
    ) {
        throw new Error("Ouvre une vidéo YouTube avant de lancer l'analyse.");
    }

    try {

        const response = await chrome.tabs.sendMessage(
            activeTab.id,
            {
                action: "GET_VISIBLE_COMMENTS"
            }
        );

        if (!response || !response.success) {
            throw new Error("Impossible de récupérer les commentaires.");
        }

        return response.comments;

    } catch (error) {

        throw new Error(
            "Le script d'extraction n'est pas disponible. Recharge la page YouTube puis réessaie."
        );
    }
}


// --------------------------------------------------
// 4. Envoyer les commentaires a l'API FastAPI
// --------------------------------------------------

async function sendCommentsToAPI(comments) {

    const response = await fetch(API_URL, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            comments: comments
        })

    });

    const data = await response.json();

    if (!response.ok) {

        const detail =
            typeof data.detail === "string"
                ? data.detail
                : JSON.stringify(data.detail);

        throw new Error(detail || `Erreur HTTP ${response.status}`);
    }

    return data;
}


// --------------------------------------------------
// 5. Bouton Analyser
// --------------------------------------------------

analyzeButton.addEventListener("click", async () => {

    analyzeButton.disabled = true;
    loadingStatus.textContent = "Extraction des commentaires...";
    pageStatus.textContent = "";

    try {

        // Recuperation des commentaires YouTube.
        const comments = await extractYouTubeComments();

        if (comments.length === 0) {

            throw new Error(
                "Aucun commentaire trouvé. Fais défiler la section des commentaires YouTube pour les charger."
            );
        }

        loadingStatus.textContent =
            `${comments.length} commentaire(s) extrait(s). Analyse en cours...`;

        // Envoi des commentaires a FastAPI.
        const data = await sendCommentsToAPI(comments);

        // Conservation des predictions.
        allPredictions = data.predictions;

        // Affichage des statistiques et des resultats.
        displayStatistics(data);
        displayResults();

        pageStatus.textContent =
            `${data.total_comments} commentaire(s) analysé(s) avec succès.`;

        loadingStatus.textContent = "";

    } catch (error) {

        loadingStatus.textContent = "";
        pageStatus.textContent = error.message;

        console.error("Erreur pendant l'analyse :", error);

    } finally {

        analyzeButton.disabled = false;
    }

});


// --------------------------------------------------
// 6. Filtrer les resultats
// --------------------------------------------------

sentimentFilter.addEventListener("change", () => {
    displayResults();
});


// --------------------------------------------------
// 7. Copier les resultats
// --------------------------------------------------

copyButton.addEventListener("click", async () => {

    if (allPredictions.length === 0) {

        pageStatus.textContent =
            "Aucun résultat à copier.";

        return;
    }

    const selectedSentiment = sentimentFilter.value;

    const filteredPredictions = allPredictions.filter(
        prediction =>
            selectedSentiment === "all" ||
            prediction.label === selectedSentiment
    );

    const textToCopy = filteredPredictions.map(prediction => {

        return [
            `Sentiment : ${prediction.label}`,
            `Confiance : ${(prediction.confidence * 100).toFixed(2)} %`,
            `Commentaire : ${prediction.comment}`
        ].join("\n");

    }).join("\n\n");

    try {

        await navigator.clipboard.writeText(textToCopy);

        pageStatus.textContent =
            "Résultats copiés dans le presse-papiers.";

    } catch (error) {

        pageStatus.textContent =
            "Impossible de copier les résultats.";

        console.error(error);
    }

});


// --------------------------------------------------
// 8. Mode sombre / mode clair
// --------------------------------------------------

themeButton.addEventListener("click", () => {

    document.body.classList.toggle("dark");

    const darkModeEnabled =
        document.body.classList.contains("dark");

    themeButton.textContent =
        darkModeEnabled ? "Mode clair" : "Mode sombre";

});
