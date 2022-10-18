const rm3 = document.getElementById("RM3");
const rm4 = document.getElementById("RM4");
const rm5 = document.getElementById("RM5");
const rm2 = document.getElementById("RM2");
const rm1 = document.getElementById("RM1");
const inv1 = document.getElementById("inv1");
const rm = document.querySelector(".rm-styling");
const home = document.getElementById("home");
const addFriend = document.getElementById("addFriend");
const accept = document.getElementById("accept");
const decline = document.getElementById("decline");
const pending = document.getElementById("pending-content");

home.addEventListener("click", () => {
    location.replace("../templates/home.html");
});


rm1.addEventListener("click", () => {
    location.replace("../templates/room_chat.html");
});

rm2.addEventListener("click", () => {
    location.replace("../templates/room_chat.html");
});

rm3.addEventListener("click", () => {
    location.replace("../templates/room_chat.html");
});

rm4.addEventListener("click", () => {
    location.replace("../templates/room_chat.html");
});

rm5.addEventListener("click", () => {
    location.replace("../templates/room_chat.html");
});

inv1.addEventListener("click", () => {
    inv1.classList.add("opacity");
});

addFriend.addEventListener("click", () => {
    location.replace("../templates/add_friend.html");
});


accept.addEventListener("click", () => {
    pending.remove();
});

decline.addEventListener("click", () => {
    pending.remove();
});