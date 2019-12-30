/*
CSS reference:
main div that contains the carousel
    .carousel

div that contains the carousel track
    .carousel_track-container

ul - contains tracks as li
    .carousel_track

li one per slide / image
    .carousel_slide

Individual img contained in slide
    .carousel_image
*/

const track = document.querySelector('.carousel_track')
const slides = Array.from(track.children)
const slideWidth = slides[0].getBoundingClientRect().width;
const numberCards = 5; // change this to make more or less cards
let previousXPos = -1; // marks previous x position of drag events

const setSlidePositionX = (slide, index) => {
    moveAmmount = slideWidth * index + 'px';
    slide.style.left = moveAmmount;
}

function dragStart(event) {
    console.info('dragStart');
    if (event.type == 'touchstart') {
        console.info('its a screen touch')
    } else {
        console.info('its a mouse touch')
        document.onmouseup = dragEnd;
        document.onmousemove = dragMove;
    }

}
function dragEnd(event) {
    console.info('dragEnd');

    // remove mouse events, nolonger dragging
    document.onmouseup = null;
    document.onmousemove = null;
}
function dragMove(event) {
    console.info('dragMove');
}


function onLoad(event) {
    // initialize track width to show numberCards 
    const trackWidth = slideWidth * numberCards;
    track.parentElement.style.width = trackWidth.toString();
}


slides.forEach( (slide, index) => {
    // set slides beside each other horizontaly
    setSlidePositionX(slide, index);
    // navigation - events (touchscreen)
    slide.addEventListener('touchstart', dragStart);
    slide.addEventListener('touchend', dragEnd);
    slide.addEventListener('touchmove', dragMove);
    // navigation - events (desktop)
    slide.addEventListener('mousedown', dragStart);
})

window.addEventListener('load', onLoad);