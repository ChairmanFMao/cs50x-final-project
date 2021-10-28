function valid() {
    let password = document.getElementById("password");
    let passwordRepeat = document.getElementById("passwordRepeat");
    
    $.get("/validatePassword?p=" + password.value + "&rp=" + passwordRepeat.value, function(out) {
        document.getElementById("passwordLetter").src = out["letter"] ? "/static/images/tick.png" : "/static/images/cross.png";
        document.getElementById("passwordNumber").src = out["number"] ? "/static/images/tick.png" : "/static/images/cross.png";
        document.getElementById("passwordLength").src = out["length"] ? "/static/images/tick.png" : "/static/images/cross.png";
        document.getElementById("passwordsMatch").src = out["match"] ? "/static/images/tick.png" : "/static/images/cross.png";
    });
}

function listeners() {
    let password = document.getElementById("password");
    let passwordRepeat = document.getElementById("passwordRepeat");
    password.addEventListener("keyup", valid);
    passwordRepeat.addEventListener("keyup", valid);
}

document.addEventListener("DOMContentLoaded", listeners);