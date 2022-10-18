const messageInput = document.getElementById("messageInput");
const messageLog = document.getElementById("message-log");
const userIcon = document.querySelector(".member-icon");
const rightPanel = document.querySelector(".right-panel");
const messages = document.querySelectorAll(".message-styling");
const home = document.getElementById("home");
messageInput.addEventListener("keypress", (e) => {
    if(e.code === "Enter"){
        // console.log(message.value);
        const messageContainer = document.createElement("div");
        const userInfo = document.createElement("p");
        const messageContent = document.createElement("div");
        const message = document.createElement("p");
        const img = document.createElement("img");
        messageContent.classList.add("d-flex", "gap10" , "align-items-center");
        img.classList.add("display-icon",  "userone-color");
        message.classList.add("message-styling", "blue", "message-width");
        img.src = "../static/images/face.png";
        userInfo.classList.add("date-padding", "font20");
        messageContainer.classList.add("message-container");
        message.innerText = messageInput.value; 
        // console.log(messageInput.value);
        userInfo.innerText = "User 1 Today: at 9:00 AM"
        messageInput.value = "";
        messageContent.appendChild(img);
        messageContent.appendChild(message);
        messageContainer.appendChild(userInfo);
        messageContainer.appendChild(messageContent);
        messageLog.appendChild(messageContainer);
        messageLog.scrollTo(0, messageLog.scrollHeight)
    }
});

userIcon.addEventListener("click", () => {
    // console.log(messages);
    rightPanel.classList.toggle("d-flex");
    rightPanel.classList.toggle("display-none");
    for(const message of messages){
        message.classList.toggle("message-width");
    }
    userIcon.classList.toggle("member-iconPos")
});

home.addEventListener("click", () => {
    location.replace("../templates/home.html");
});
