const box = document.getElementsByClassName('typing-text')[0];
const str = box.innerText;
let i = 0;
box.innerText = '';
const typing = setInterval(function () {
    box.innerText += str[i++];
    i >= str.length && clearInterval(typing);
}, 100);