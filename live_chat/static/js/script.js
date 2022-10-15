const button = document.getElementById("sendMessage");
const message = document.getElementById("message")
const socket = io.connect("http://127.0.0.1:5000");    

socket.on("connect", () => {
    console.log("we're connected");
});

function sendMessage(){
    console.log('clicking');
    console.log(message.value);
    socket.emit("message", message.value);
}

message.addEventListener("keypress", (e) => {
    if(e.code === "Enter"){
        console.log(message.value);
        socket.emit("message", message.value)
        message.value = "";
    }
})

socket.on('message', (message) => {
    console.log("Message logged: ", message);
});


button.addEventListener('click', sendMessage);

