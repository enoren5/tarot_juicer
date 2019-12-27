const currentSelection = localStorage.getItem('showProperty');

if (currentSelection === 'content') {
  document.querySelector('.regular-btn').style.backgroundColor = '#e52424';
  document.querySelector('.study-btn').style.backgroundColor = '#e94646';

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
  document.querySelector('.regular-btn').style.backgroundColor = '#e94646';
  document.querySelector('.study-btn').style.backgroundColor = '#e52424';

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
  document.querySelector('.regular-btn').style.backgroundColor = '#e52424';
  document.querySelector('.study-btn').style.backgroundColor = '#e94646';

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

  document.querySelector('.regular-btn').style.backgroundColor = '#e94646';
  document.querySelector('.study-btn').style.backgroundColor = '#e52424';

  const contents = document.querySelectorAll('.content');
  contents.forEach((content) => {
    content.style.display = 'none';
    content.style.opacity = '0';
  });

  // #e52424

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
