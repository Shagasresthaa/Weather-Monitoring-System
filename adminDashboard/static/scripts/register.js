function myFunction1() {
    var x = document.getElementById("passwd");
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
}