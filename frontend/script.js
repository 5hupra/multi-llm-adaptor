async function sendMessage() {

    const messageInput = document.getElementById("message");
    const providerSelect = document.getElementById("provider");
    const responsesBox = document.getElementById("responses");
    const sendButton = document.querySelector("button");

    const message = messageInput.value.trim();
    const provider = providerSelect.value;

    if (!message) return;

    sendButton.disabled = true;
    sendButton.innerText = "Thinking...";

    responsesBox.innerHTML += `
        <div class="msg"><b>You:</b> ${message}</div>
    `;

    messageInput.value = "";

    const aiDiv = document.createElement("div");
    aiDiv.className = "msg";
    aiDiv.innerHTML = "<b>AI:</b> ";
    responsesBox.appendChild(aiDiv);

    try {
        const response = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                message: message,
                provider: provider,
                stream: true
            })
        });
        if (!response.ok) {
            const errText = await response.text();
            throw new Error(errText || `HTTP ${response.status}`);
        }


        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value);
            aiDiv.innerHTML += chunk;
            responsesBox.scrollTop = responsesBox.scrollHeight;
        }

    } catch (error) {
        console.error(error);
        aiDiv.innerHTML += "Error receiving response";
    }

    sendButton.disabled = false;
    sendButton.innerText = "Send";
}