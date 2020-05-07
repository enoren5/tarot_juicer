// const date = new Date();
// document.querySelector('.year').innerHTML = date.getFullYear();

setTimeout(function () {
  $("#message").fadeOut("slow");
}, 1000);

function navbarButton() {
  const button = document.getElementById("toggler-button");
  const span = button.querySelector("span");
  span.classList.toggle("navbar-toggler-icon");
  span.classList.toggle("fa");
  span.classList.toggle("fa-times");
  span.classList.toggle("fa-2x");
}
