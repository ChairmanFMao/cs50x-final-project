function valid() {
    let password = document.getElementById("password");
    let passwordRepeat = document.getElementById("passwordRepeat");
    let button = document.getElementById("log-in-button");
    let allValid = true;
    let result = null;
    $.ajax({url: "/validatePassword?p=" + password.value + "&rp=" + passwordRepeat.value, type:"get", dataType:"html", async:false, success: function(data) {
        let passwordArray = [document.getElementById("passwordLetter"), document.getElementById("passwordNumber"), document.getElementById("passwordLength"), document.getElementById("passwordsMatch")];
        passwordArray[0].src = data["letter"] ? "/static/images/tick.png" : "/static/images/cross.png";
        passwordArray[1].src = data["number"] ? "/static/images/tick.png" : "/static/images/cross.png";
        passwordArray[2].src = data["length"] ? "/static/images/tick.png" : "/static/images/cross.png";
        passwordArray[3].src = data["match"] ? "/static/images/tick.png" : "/static/images/cross.png";
        if (document.getElementById("termsAndConditions").checked == false) {
            allValid = false;
        }
    }});
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