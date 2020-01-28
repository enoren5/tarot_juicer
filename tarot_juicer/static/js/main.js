// const date = new Date();
// document.querySelector('.year').innerHTML = date.getFullYear();

setTimeout(function() {
  $('#message').fadeOut('slow')
}, 3000)

function navbarButton(button) {
  const span = button.querySelector('span')
  span.classList.toggle('navbar-toggler-icon')
  span.classList.toggle('fa', 'fa-times', 'fa-3x')
  span.classList.toggle('fa-times')
  span.classList.toggle('fa-4x')
}
