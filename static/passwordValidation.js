function valid() {
    let password = document.getElementById("password");
    let passwordRepeat = document.getElementById("passwordRepeat");
    let button = document.getElementById("log-in-button");
    let allValid = true;
    let result = null;
    $.get("/validatePassword?p=" + password.value + "&rp=" + passwordRepeat.value, function(valid) {
        let currentValid = true;
        let passwordArray = [document.getElementById("passwordLetter"), document.getElementById("passwordNumber"), document.getElementById("passwordLength"), document.getElementById("passwordsMatch")];
        for (let i = 0; i < 4; i++) {
            passwordArray[i].src = valid[i] ? "/static/images/tick.png" : "/static/images/cross.png";
            currentValid = currentValid && valid[i];
        }
        currentValid = currentValid && document.getElementById("termsAndConditions").checked;
        function a(currentValid){
            result =  currentValid;
        }
        a(currentValid);
    });
    console.log(result);
    $.get("/validateUsername?q=" + username.value, function(good) {
        let currentValid = true;
        currentValid = currentValid && (good.length == 0 && username.value.length >= 4)
        return currentValid;
    });
    button.disabled = !allValid;
}

function listeners() {
    let password = document.getElementById("password");
    let passwordRepeat = document.getElementById("passwordRepeat");
    let username = document.getElementById("username");
    password.addEventListener("keyup", valid);
    passwordRepeat.addEventListener("keyup", valid);
    username.addEventListener("keyup", valid);
}

document.addEventListener("DOMContentLoaded", listeners);