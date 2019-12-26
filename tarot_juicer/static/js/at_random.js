var reload = function() {
  window.location.reload();
};

const currentSelection = localStorage.getItem('showProperty');

if (currentSelection === 'content') {
  const bullets = document.querySelectorAll('.bullets');
  bullets.forEach((bullet) => {
    bullet.style.display = 'none';
    bullet.style.opacity = '0';
  });

  const contents = document.querySelectorAll('.content');
  contents.forEach((content) => {
    content.style.display = 'block';
    content.style.opacity = '1';
  });
} else if (currentSelection === 'bullet') {
  const contents = document.querySelectorAll('.content');
  contents.forEach((content) => {
    content.style.display = 'none';
    content.style.opacity = '0';
  });

  const bullets = document.querySelectorAll('.bullets');
  bullets.forEach((bullet) => {
    bullet.style.display = 'block';
    bullet.style.opacity = '1';
  });
}

document.querySelector('.regular-btn').addEventListener('click', function() {
  localStorage.setItem('showProperty', 'content');
  const bullets = document.querySelectorAll('.bullets');
  bullets.forEach((bullet) => {
    bullet.style.display = 'none';
    bullet.style.opacity = '0';
  });

  const contents = document.querySelectorAll('.content');
  contents.forEach((content) => {
    content.style.display = 'block';
    content.style.opacity = '1';
  });
});
document.querySelector('.study-btn').addEventListener('click', function() {
  localStorage.setItem('showProperty', 'bullet');

  const contents = document.querySelectorAll('.content');
  contents.forEach((content) => {
    content.style.display = 'none';
    content.style.opacity = '0';
  });

  const bullets = document.querySelectorAll('.bullets');
  bullets.forEach((bullet) => {
    bullet.style.display = 'block';
    bullet.style.opacity = '1';
  });
});

var galileoImg = function() {
  const galileo = document.getElementById(`galileo-content`);
  if (galileo.style.display === 'none') {
    galileo.style.display = 'block';
  } else {
    galileo.style.display = 'none';
  }
};

var flossImg = function() {
  const galileo = document.getElementById(`f-loss-content`);
  if (galileo.style.display === 'none') {
    galileo.style.display = 'block';
  } else {
    galileo.style.display = 'none';
  }
};

var stPaulImg = function() {
  const galileo = document.getElementById(`st-paul-content`);
  if (galileo.style.display === 'none') {
    galileo.style.display = 'block';
  } else {
    galileo.style.display = 'none';
  }
};
