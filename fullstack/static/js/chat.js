const chatOpen = document.getElementById("chat-open");
const sendChatMessageBtn = document.getElementById("chat-send-message");
const chatInput = document.getElementById("chat-input");
const chatWindow = document.getElementById("chat-window");
const chatClose = document.getElementById("chat-close");
let chatSocket = null

function scrollToBottom() {
    chatWindow.scrollTop = chatWindow.scrollHeight
}

async function getChatData() {
    const response = await fetch('/chat/get-chat-data/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    })

    const data = await response.json();
    return data;
}

function onChatMessage(data) {
    if (data.type === 'chat_message') {
        if (!data.is_agent) {
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

chatClose.onclick = function(e) {
    chatSocket.close();
}

function sendMessage() {
    chatSocket.send(JSON.stringify({
        'type': 'message',
        'content': chatInput.value,
        'is_agent': false
    }))

    chatInput.value = ''
}

chatOpen.onclick = async function(e) {
    chatInput.focus();
    data = await getChatData();
    chatWindow.textContent = '';
    for (i in data.messages) {
        data.messages[i]['type'] = 'chat_message'
        onChatMessage(data.messages[i]);
    }

    chatSocket = new WebSocket(`ws://${window.location.host}/ws/${data.pk}/`);
    console.log(chatSocket);

    chatSocket.onmessage = function(e) {
        onChatMessage(JSON.parse(e.data))
    }
    scrollToBottom()
}

function checkInput() {
    if (chatInput.value === '') {
        sendChatMessageBtn.disabled = true;
    } else {
        sendChatMessageBtn.disabled = false;
    }
}

chatInput.onkeyup = function(e) {
    if (e.keyCode == 13 && chatInput.value !== '') {
        sendMessage()
        checkInput()
    }
}

chatInput.addEventListener('input', checkInput)

sendChatMessageBtn.onclick = function(e) {
    e.preventDefault()
    if (chatInput.value !== '') {
        sendMessage()
    }
    return false
}


function handleKeyPress(event) {
    if (event.keyCode === 27 && chatSocket && chatSocket.readyState === 1) {
        chatSocket.close();
    }
}

document.addEventListener('keydown', handleKeyPress);