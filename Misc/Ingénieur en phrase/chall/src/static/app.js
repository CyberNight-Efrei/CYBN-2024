const socket = io("/chat");

function addMessage(user, message) {
    const messagesContainer = document.querySelector(".messages");
    const messageElement = document.createElement("div");
    messageElement.classList.add("message");
    messageElement.classList.add(`message-${user}`);
    messageElement.innerText = message;
    messagesContainer.appendChild(messageElement);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

socket.on('message', (data) => {
    if (data.type === "serverMessage") {
        addMessage("server", data.message);
    }
})

socket.on('connect', () => {
    console.log('connected');
});

function sendUserMessage(message) {
    addMessage("user", message);
    socket.emit('message', {type: 'userMessage', message: message});
}

document.querySelector("#chat_input").addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        const message = event.target.value;
        event.target.value = "";
        sendUserMessage(message);
    }
});

document.querySelector("#chat_send").addEventListener("click", (event) => {
    const message = document.querySelector("#chat_input").value;
    document.querySelector("#chat_input").value = "";
    sendUserMessage(message);
});
