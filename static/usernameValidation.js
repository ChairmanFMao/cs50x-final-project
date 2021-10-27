function listeners() {
    let username = document.getElementById("username");
    username.addEventListener("keyup", function() {
        $.get("/validateUsername?q=" + username.value, function(valid) {
            let button = document.getElementById("log-in-button");
            if (valid.length != 1) {
                button.disabled = true;
            }
            else {
                button.disabled = false;
            }
        })
    });
}





document.addEventListener("DOMContentLoaded", listeners);