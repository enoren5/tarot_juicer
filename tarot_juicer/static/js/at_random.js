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
    p.classList.remove("fadeInRightBig");
    h1.classList.remove("fadeInRightBig");
    img.classList.add("show-img-shadow");
    galileo.style.display = "block";
  } else {
    p.classList.add("fadeInRightBig");
    h1.classList.add("fadeInRightBig");
    img.classList.remove("show-img-shadow");
    setTimeout(() => {
      galileo.style.display = "none";
    }, 1000);
  }
};

var flossImg = function(li) {
  const floss = document.getElementById(`f-loss-content`);
  let img = li.querySelector("img");
  const h1 = floss.querySelector("h1");
  const p = floss.querySelector("p");

  if (floss.style.display === "none") {
    floss.style.display = "block";
    img.classList.add("show-img-shadow");
    p.classList.remove("fadeInRightBig");
    h1.classList.remove("fadeInRightBig");
  } else {
    p.classList.add("fadeInRightBig");
    h1.classList.add("fadeInRightBig");
    img.classList.remove("show-img-shadow");
    setTimeout(() => {
      floss.style.display = "none";
    }, 500);
  }
};

var stPaulImg = function(li) {
  const stPaul = document.getElementById(`st-paul-content`);
  let img = li.querySelector("img");
  const h1 = stPaul.querySelector("h1");
  const p = stPaul.querySelector("p");

  if (stPaul.style.display === "none") {
    stPaul.style.display = "block";
    p.classList.remove("fadeInRightBig");
    h1.classList.remove("fadeInRightBig");
    img.classList.add("show-img-shadow");
  } else {
    p.classList.add("fadeInRightBig");
    h1.classList.add("fadeInRightBig");
    img.classList.remove("show-img-shadow");
    setTimeout(() => {
      stPaul.style.display = "none";
    }, 500);
  }
};
