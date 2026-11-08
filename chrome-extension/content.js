(() => {
    // Eviter de charger plusieurs fois le meme script.
    if (globalThis.youtubeSentimentLoaded) {
        return;
    }

    globalThis.youtubeSentimentLoaded = true;

    function extractComments() {

        // Recuperer les textes des commentaires YouTube.
        const elements = document.querySelectorAll(
            "ytd-comment-thread-renderer #content-text, " +
            "ytd-comment-view-model #content-text"
        );

        const comments = [];
        const seen = new Set();

        elements.forEach((element) => {

            const comment = element.innerText
                .replace(/\s+/g, " ")
                .trim();

            // Ignorer les commentaires vides et les doublons.
            if (comment.length > 0 && !seen.has(comment)) {
                seen.add(comment);
                comments.push(comment);
            }

        });

        // L'API accepte au maximum 100 commentaires par requete.
        return comments.slice(0, 100);
    }

    // Ecouter les messages envoyes par popup.js.
    chrome.runtime.onMessage.addListener(
        (message, sender, sendResponse) => {

            if (message.action === "GET_VISIBLE_COMMENTS") {

                const comments = extractComments();

                sendResponse({
                    success: true,
                    count: comments.length,
                    comments: comments
                });

            }

        }
    );

})();
