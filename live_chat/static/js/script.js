const message = document.getElementById("message")
const socket = io.connect("http://127.0.0.1:5000");    
const table = document.getElementById("messages");
socket.on("connect", () => {
    console.log("we're connected");
});


message.addEventListener("keypress", (e) => {
    if(e.code === "Enter"){
        // console.log(message.value);
        socket.emit("message", message.value)
        message.value = "";
    }
})

socket.on('message', (message) => {
    console.log("Message logged: ", message);
    const tableRow = document.createElement("tr");
    const tableItem = document.createElement("td");
    tableItem.innerText = message;
    tableItem.classList.add('text-warning');
    tableRow.appendChild(tableItem);
    table.appendChild(tableRow);

});



