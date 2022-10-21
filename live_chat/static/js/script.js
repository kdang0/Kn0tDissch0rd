const socket = io.connect("http://127.0.0.1:5000");    
// const table = document.getElementById("messages");
const form = document.querySelector('form');
socket.on("connect", () => {
    socket.emit('join_room', {
        name: user_name,
        room_id: room_id,
        user_id: user_id
    });
    initiateMessage();
    // loadMessages();
});


socket.on('join_room', data => {
    console.log(`${data.name} joined the chat`)
});

socket.on('send_message', data => {
    createMessage(data)
});

socket.on('load_messages', data =>{
    for(let msg of data.messages){
        createMessage(msg);
    }
})

messageInput.addEventListener("keypress", (e) => {
    if(e.code === "Enter"){
        // console.log(message.value);
        initiateMessage()

    }
})

// socket.on('message', (message) => {
//     console.log("Message logged: ", message);
//     const tableRow = document.createElement("tr");
//     const tableItem = document.createElement("td");
//     tableItem.innerText = message;
//     tableItem.classList.add('text-warning');
//     tableRow.appendChild(tableItem);
//     table.appendChild(tableRow);

// });

function initiateMessage(){
    // form.reset();
    messageInput.focus();
    form.onsubmit = e => {
        e.preventDefault();
        console.log(messageInput.value);
        console.log("HOHOHOHOHO");
        handleMessage();
        form.reset();
    }
}

function handleMessage(){
    socket.emit('send_message', {
        name: user_name,
        room_id: room_id,
        user_id: user_id,
        message_content: messageInput.value.trim() 
    });
    initiateMessage();
}


function createMessage(msg){
    const messageContainer = document.createElement("div");
    const userInfo = document.createElement("p");
    const messageContent = document.createElement("div");
    const message = document.createElement("p");
    const img = document.createElement("img");
    messageContent.classList.add("d-flex", "gap10" , "align-items-center");
    img.classList.add("display-icon",  "userone-color");
    message.classList.add("message-styling", "message-width");
    img.src = img_src;
    userInfo.classList.add("date-padding", "font20");
    messageContainer.classList.add("message-container");
    message.innerText = msg["content"]; 
    // console.log(messageInput.value);
    userInfo.innerText = msg["user_name"] + " " + msg["created_at"]
    messageContent.appendChild(img);
    messageContent.appendChild(message);
    messageContainer.appendChild(userInfo);
    messageContainer.appendChild(messageContent);
    messageLog.appendChild(messageContainer);
    messageLog.scrollTo(0, messageLog.scrollHeight)
}

// function createUserJoined(user_name){
//     const
// }

function loadMessages(){
    socket.emit('load_messages', {
        room_id : room_id
    });
}

