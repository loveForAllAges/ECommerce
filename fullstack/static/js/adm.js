const sendChatMessageBtn = document.getElementById("agent-chat-send-message");
const chatInput = document.getElementById("agent-chat-input");
const chatWindow = document.getElementById("agent-chat-window");
const chatSocket = new WebSocket(`ws://${window.location.host}/ws/admin_chat/`);

scrollToBottom()

function scrollToBottom() {
    chatWindow.scrollTop = chatWindow.scrollHeight
}

function checkInput() {
    if (chatInput.value === '') {
        sendChatMessageBtn.disabled = true;
    } else {
        sendChatMessageBtn.disabled = false;
    }
}

chatInput.addEventListener('input', checkInput)

function onChatMessage(data) {
    if (data.type === 'chat_message') {
        if (data.is_agent) {
            chatWindow.innerHTML += `
            <div class="ml-[20%] flex justify-end">
                <div class="mb-2 text-gray-900 shadow-sm bg-gray-200 rounded-xl p-2 inline-block text-sm">
                    <span class="">${data.content}</span>
                    <span class="-mb-1 block w-full text-xs text-gray-500 text-end">${data.created_at_formatted}</span>
                </div>
            </div>
            `
        } else {
            chatWindow.innerHTML += `
            <div class="max-w-[80%]">
                <div class="mb-2 bg-white shadow-sm text-gray-900 rounded-xl p-2 inline-block text-sm">
                    <span class="">${data.content}</span>
                    <span class="-mb-1 block w-full text-xs text-gray-400 text-end">${data.created_at_formatted}</span>
                </div>
            </div>
            `
        }
    } else if (data.type === 'chat_info') {
        chatWindow.innerHTML += `
        <div class="text-center">
            <div class="mb-2 text-gray-500 p-2 inline-block text-xs">
                <span class="">${data.content}</span>
            </div>
        </div>
        `
    }
    scrollToBottom()
}

chatSocket.onmessage = function(e) {
    onChatMessage(JSON.parse(e.data))
}

chatInput.onkeyup = function(e) {
    if (e.keyCode == 13 && chatInput.value !== '') {
        sendMessage()
        checkInput()
    }
}

function sendMessage() {
    chatSocket.send(JSON.stringify({
        'type': 'message',
        'content': chatInput.value,
        'is_agent': true
    }))

    chatInput.value = ''
}

sendChatMessageBtn.onclick = function(e) {
    e.preventDefault()
    if (chatInput.value !== '') {
        sendMessage()
    }
    return false
}

chatInput.onkeyup = function(e) {
    if (e.keyCode == 13 && chatInput.value !== '') {
        sendMessage()
        checkInput()
    }
}