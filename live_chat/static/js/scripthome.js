
// const inv1 = document.getElementById("inv1");
// const rm = document.querySelector(".rm-styling");
// // const home = document.getElementById("home");
// const addFriend = document.getElementById("addFriend");
// const accept = document.getElementById("accept");
// const decline = document.getElementById("decline");
// const pending = document.getElementById("pending-content");

// home.addEventListener("click", () => {
//     location.replace("../templates/home.html");
// });


// rm1.addEventListener("click", () => {
//     location.replace("../templates/room_chat.html");
// });

// rm2.addEventListener("click", () => {
//     location.replace("../templates/room_chat.html");
// });

// rm3.addEventListener("click", () => {
//     location.replace("../templates/room_chat.html");
// });

// rm4.addEventListener("click", () => {
//     location.replace("../templates/room_chat.html");
// });

// rm5.addEventListener("click", () => {
//     location.replace("../templates/room_chat.html");
// });

// inv1.addEventListener("click", () => {
//     inv1.classList.add("opacity");
// });

// addFriend.addEventListener("click", () => {
//     location.replace("../templates/add_friend.html");
// });


// accept.addEventListener("click", () => {
//     pending.remove();
// });

// decline.addEventListener("click", () => {
//     pending.remove();
// });
const socket = io.connect("http://127.0.0.1:5000");    
const joinRoom = document.getElementById("join-room");
const form = document.querySelector('form');
socket.on("connect", () => {
    // socket.emit('join_room', {
    //     name: user_name,
    //     room_id: room_id,
    //     user_id: user_id
    // });
    initiateJoin();
    // loadMessages();
});

socket.on('joining_room', data => {
    // console.log(`${data.name} joined the chat`);
    console.log(data);
    window.location.replace(`/rm/${data.room_name}/${data.room_id}`);
});

socket.on('update_availability', () => {
    location.reload();
})

function handleJoin(){
    socket.emit("joining_room", {
        "room_id" : joinRoom.value
    }); 
}

function initiateJoin(){
    console.log(joinRoom.value);
    form.onsubmit = e => {
        e.preventDefault();
        handleJoin();
    }
}


