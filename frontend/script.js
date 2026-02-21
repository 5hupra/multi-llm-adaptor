async function sendMessage() {

    const messageInput = document.getElementById("message");
    const providerSelect = document.getElementById("provider");
    const responsesBox = document.getElementById("responses");

    const message = messageInput.value.trim();
    const provider = providerSelect.value;

    if (!message) return;

    responsesBox.innerHTML += `
        <div class="msg"><b>You:</b> ${message}</div>
    `;

    messageInput.value = "";

    try {
        const response = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                message: message,
                provider: provider
            })
        });

        const data = await response.json();

        
        const reply = data.response?.text || "No response";

        responsesBox.innerHTML += `
            <div class="msg">
                <b>AI:</b> ${reply}
                <div class="meta">
                    Provider: ${data.provider} |
                    Fallback: ${data.fallback}
                </div>
            </div>
        `;

    } catch (error) {
        console.error(error);
        responsesBox.innerHTML += `
            <div class="msg">Error connecting to backend</div>
        `;
    }
}