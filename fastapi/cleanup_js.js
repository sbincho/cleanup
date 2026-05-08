var client_id = Date.now(); // 고유한 클라이언트 ID 생성
document.querySelector("#ws-id").textContent = client_id; // 클라이언트 ID 표시

var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`); // 웹소켓 연결

ws.onmessage = function(event) {
    var messages = document.getElementById('messages');
    var message = document.createElement('li');
    var content = document.createTextNode(event.data);
    message.appendChild(content);
    
    // 메시지 유형에 따라 스타일 추가
    if (event.data.startsWith("Client #")) {
        message.className = 'message received'; // 수신된 메시지 스타일
    } else {
        message.className = 'message sent'; // 송신된 메시지 스타일
    }
    
    messages.prepend(message);
};

function sendMessage(event) {
    var input = document.getElementById("messageText");
    if (input.value.trim() !== '') { // 공백만 있는 메시지는 전송하지 않음
        ws.send(input.value);
        input.value = '';
        updateCharCount();
        updateButtonState();
    }
    event.preventDefault(); // 폼 제출 방지
}

// 문자 수와 버튼 상태 업데이트
document.getElementById('messageText').addEventListener('input', function() {
    updateCharCount();
    updateButtonState();
});

function updateCharCount() {
    var count = document.getElementById('messageText').value.length;
    document.querySelector('.char-count').textContent = `${count} / 300`;
}

function updateButtonState() {
    var button = document.querySelector('.chat-form button');
    var input = document.getElementById('messageText');
    if (input.value.length > 0) {
        button.classList.add('active');
    } else {
        button.classList.remove('active');
    }
}

const socket = new WebSocket("ws://localhost:8000");

socket.onmessage = function(event) {
    const message = event.data;
    const lines = message.split('\n');
    const formattedMessage = lines.join('<br>'); // 줄바꿈을 <br>로 변환하여 HTML에서 제대로 표시되도록 함
    document.getElementById("messageContainer").innerHTML += formattedMessage + '<br>';
};