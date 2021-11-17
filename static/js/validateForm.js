function validate() {
    var pass = document.getElementById("password").value;
    var cpass = document.getElementById("cPassword").value;
    if (pass == cpass) {
        return true;
    } else {
        alert("Passwords Doesn't match");
        return false;
    }
}