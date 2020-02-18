const currentSelection = localStorage.getItem("showProperty");

if (currentSelection === "bullet") {
  document.querySelector(".regular-btn").style.backgroundColor = "#e94646";
  document.querySelector(".study-btn").style.backgroundColor = "#e52424";

  const contents = document.querySelectorAll(".content");
  contents.forEach(content => {
    content.style.display = "none";
    content.style.opacity = "0";
  });

  const bullets = document.querySelectorAll(".bullets");
  bullets.forEach(bullet => {
    bullet.style.display = "block";
    bullet.style.opacity = "1";
  });
} else {
  document.querySelector(".regular-btn").style.backgroundColor = "#e52424";
  document.querySelector(".study-btn").style.backgroundColor = "#e94646";

  const bullets = document.querySelectorAll(".bullets");
  bullets.forEach(bullet => {
    bullet.style.display = "none";
    bullet.style.opacity = "0";
  });

  const contents = document.querySelectorAll(".content");
  contents.forEach(content => {
    content.style.display = "block";
    content.style.opacity = "1";
  });
}

document.querySelector(".regular-btn").addEventListener("click", function() {
  document.querySelector(".regular-btn").style.backgroundColor = "#e52424";
  document.querySelector(".study-btn").style.backgroundColor = "#e94646";

  localStorage.setItem("showProperty", "content");
  const bullets = document.querySelectorAll(".bullets");
  bullets.forEach(bullet => {
    bullet.style.display = "none";
    bullet.style.opacity = "0";
  });

  const contents = document.querySelectorAll(".content");
  contents.forEach(content => {
    content.style.display = "block";
    content.style.opacity = "1";
  });
});

document.querySelector(".study-btn").addEventListener("click", function() {
  localStorage.setItem("showProperty", "bullet");

  document.querySelector(".regular-btn").style.backgroundColor = "#e94646";
  document.querySelector(".study-btn").style.backgroundColor = "#e52424";

  const contents = document.querySelectorAll(".content");
  contents.forEach(content => {
    content.style.display = "none";
    content.style.opacity = "0";
  });

  const bullets = document.querySelectorAll(".bullets");
  bullets.forEach(bullet => {
    bullet.style.display = "block";
    bullet.style.opacity = "1";
  });
});

var galileoImg = function(li) {
  const galileo = document.getElementById(`galileo-content`);
  const h1 = galileo.querySelector("h1");
  const p = galileo.querySelector("p");
  let img = li.querySelector("img");

  if (galileo.style.display === "none") {
    p.classList.remove("fadeOutRight");
    h1.classList.remove("fadeOutRight");
    img.classList.add("show-img-shadow");
    $('#galileo-content').slideToggle();
  } else {
    p.classList.add("fadeOutRight");
    h1.classList.add("fadeOutRight");
    img.classList.remove("show-img-shadow");
    $('#galileo-content').slideToggle();
  }
};

var flossImg = function(li) {
  const floss = document.getElementById(`f-loss-content`);
  let img = li.querySelector("img");
  const h1 = floss.querySelector("h1");
  const p = floss.querySelector("p");

  if (floss.style.display === "none") {
    img.classList.add("show-img-shadow");
    p.classList.remove("fadeOutRight");
    h1.classList.remove("fadeOutRight");
    $('#f-loss-content').slideToggle();
  } else {
    p.classList.add("fadeOutRight");
    h1.classList.add("fadeOutRight");
    img.classList.remove("show-img-shadow");
    $('#f-loss-content').slideToggle();
  }
};

var stPaulImg = function(li) {
  const stPaul = document.getElementById(`st-paul-content`);
  let img = li.querySelector("img");
  const h1 = stPaul.querySelector("h1");
  const p = stPaul.querySelector("p");

  if (stPaul.style.display === "none") {
    p.classList.remove("fadeOutRight");
    h1.classList.remove("fadeOutRight");
    img.classList.add("show-img-shadow");
    $('#st-paul-content').slideToggle();
  } else {
    p.classList.add("fadeOutRight");
    h1.classList.add("fadeOutRight");
    img.classList.remove("show-img-shadow");
    $('#st-paul-content').slideToggle();
  }
};
