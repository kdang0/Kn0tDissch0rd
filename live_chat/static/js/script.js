const socket = io.connect("http://127.0.0.1:5000");    
const form = document.querySelector('form');
const userList = document.querySelector('.user-list');
const leave = document.querySelector(".leave-btn");
socket.on("connect", () => {
    socket.emit('join_room', {
        name: user_name,
        room_id: room_id,
        user_id: user_id
    });
    initiateMessage();
    initiateLeave();
    // loadMessages();
});

socket.on('join_room', data => {
    console.log(`${data.name} joined the chat`);
    createUsers(data.users);
});

socket.on('leave_room', data => {
    console.log(`${data.user_name} left the chat`);
    createUsers(data["users"]);
})

socket.on('send_message', data => {
    console.log(data);
    createMessage(data)
});

socket.on('load_messages', data =>{
    for(let msg of data.messages){
        createMessage(msg);
    }
});

socket.on('delete_room', () => {
    window.location.replace("/home");
});


function initiateLeave(){
    leave.onclick = e => {
        handleLeave();
    }
}


function initiateMessage(){
    // form.reset();
    messageInput.focus();
    form.onsubmit = e => {
        e.preventDefault();
        handleMessage();
        form.reset();
    }
}

function handleLeave(){
    socket.emit('leave', {
        room_id: room_id
    })
}

function handleMessage(){
    socket.emit('send_message', {
        name: user_name,
        room_id: room_id,
        user_id: user_id,
        message_content: messageInput.value.trim() 
    });
}

function deleteChildren(parent){
    while(parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}

function createUsers(content){
    deleteChildren(userList);
    for(user of content){
        const userContainer = document.createElement("div");
        userContainer.classList.add("user-styling", "d-flex", "justify-content-center", "align-items-center", "usertwo-color")
        const userItem = document.createElement("p");
        userItem.classList.add("font20");
        userItem.innerText = user["user_name"];
        userContainer.appendChild(userItem);
        userList.append(userContainer);
    }
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
    userInfo.innerText = msg["user_name"] + " " + msg["created_at"]
    messageContent.appendChild(img);
    messageContent.appendChild(message);
    messageContainer.appendChild(userInfo);
    messageContainer.appendChild(messageContent);
    messageLog.appendChild(messageContainer);
    messageLog.scrollTo(0, messageLog.scrollHeight)
}


function loadMessages(){
    socket.emit('load_messages', {
        room_id : room_id
    });
}

