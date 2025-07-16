// File: static/app.js

document.addEventListener('DOMContentLoaded', () => {
    const socket = io("http://localhost:5000");

    socket.on("connect", () => {
        console.log("✅ WebSocket connected");
    });

    socket.on("disconnect", () => {
        console.log("❌ WebSocket disconnected");
    });

    socket.on("subtitles", (data) => {
        const originalElem = document.getElementById("original");
        const translatedElem = document.getElementById("translated");

        if (originalElem && translatedElem) {
            originalElem.textContent = data.original || "No original text";
            translatedElem.textContent = data.translated || "No translation available";
        }
    });

    const startButton = document.getElementById("startButton");

    if (startButton) {
        let isTranslating = false;

        startButton.addEventListener('click', () => {
            if (!isTranslating) {
                fetch('/start', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                })
                .then(res => res.json())
                .then(data => {
                    console.log("Translation started:", data);
                    isTranslating = true;
                    startButton.textContent = "⏸️ Pause Translation";
                    startButton.disabled = true; // remove if you want toggle pause logic
                })
                .catch(err => {
                    console.error("Error starting translation:", err);
                    alert("Failed to start translation.");
                });
            }
        });
    }
});
