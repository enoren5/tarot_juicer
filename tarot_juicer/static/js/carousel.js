/* .carousel {

contains the slides
.carousel_slider

each slide is a flex child, acts as cell to contain images
.slide


individual slide image / card
.carousel_slider img

*/

// Change this to control how many cards are visible on carousel at one time
const cardsToDisplay = 5;

function pixelsToValue(pixels) {
    return pixels.length ? 
        parseFloat(pixels.substring(0, pixels.length - 2)) :
        0;
}

/* Helper function that takes the ammount moved during drag
  and the size of the slide, determines how much to add
  or substract from current movement to round or snap back
  / forward next / previous card.   Hard to explain */
function getSnapShiftDelta(moved, slideWidth) {
    abs_m = Math.abs(moved)
    abs_s = Math.abs(slideWidth)
    fraction = ((moved/slideWidth) - Math.trunc(moved/slideWidth))
    d1 = fraction * slideWidth
    d2 = Math.round(slideWidth-d1)
    deltaX = Math.abs(d1) < Math.abs(d2) ? d1 : d2
    deltaX = Math.abs(deltaX)
    if (Math.round(fraction) == 1) {
        direction = 1
        if (moved < 0) {
            deltaX = deltaX * -1
        } else {
            deltaX = deltaX
        }
    } else {
        direction = -1
        if (moved < 0) {
            deltaX = deltaX
        } else {
            deltaX = deltaX * -1
        }
    }
    return Math.round(deltaX);
}

function onLoad(event) {
    const slider = document.querySelector('.carousel_slider')
    const slides = document.querySelectorAll('.slide')
    carousel(slider, slides);

}

// Contains all carousel related code, did not use classes for older android support
function carousel(slider, slides) {
    let sliderWidth;
    let startX;
    let scrollLeft;
    let isDown = false;
    let slideWidth = slides[0].offsetWidth;
    let prevShift = 0;
    let moved = 0;
    let shiftAmmount = 0;
    let cardsShifted = 0;
    const computedTrackWidth = window.getComputedStyle(slider).width;
    firstSlide = slides[0],
    lastSlide = slides[slides.length - 1],
    cloneFirst = firstSlide.cloneNode(true),
    cloneLast = lastSlide.cloneNode(true),

    // Clone first and last slide - so we can scroll from start
    slider.appendChild(cloneFirst);
    slider.insertBefore(cloneLast, firstSlide);

    // Start with cloned first card off screen
    slider.style.transform = `translateX(-${slideWidth}px)`
    

    // navigation - events (desktop)
    slider.addEventListener('mousedown', dragStart);
    slider.addEventListener('mouseup', dragEnd);
    slider.addEventListener('mousemove', dragMove);
    slider.addEventListener('mouseleave', dragEnd);
    // navigation - touch events (mobile)
    slider.addEventListener('touchstart', dragStart);
    slider.addEventListener('touchend', dragEnd);
    slider.addEventListener('touchmove', dragMove);

    // handle touch / mouse drag begin
    function dragStart(event) {
        slideWidth = slides[0].offsetWidth;
        totalMoved = 0;
        if (event.type.includes('touch')) {
            clientX = event.touches[0].clientX
        } else {
            isDown = true;
            startX = event.clientX;
            moved = 0;
            // scrollLeft = slider.scrollLeft;
            scrollLeft = pixelsToValue(slider.style.left);
            // scrollLeft = pixelsToValue(slider.style.left);
        }

    }

    // touch / mouse up (drag end)
    function dragEnd(event) {
        if (!isDown) {
            return false;
        }
        isDown = false;
        cardsShifted = 0;
        prevShift = 0;
        // Change moved to current left
        currentLeft = pixelsToValue(slider.style.left);
        snapDelta = getSnapShiftDelta(moved, slideWidth)
        newLeft = currentLeft + snapDelta + 'px';
        console.info({currentLeft, snapDelta, newLeft})
        slider.style.left = newLeft;

    }

    // touch / mouse drag in progress
    function dragMove(event) {
        element = event.target;
        if (event.type.includes('touch')) {
            
        } else if (!isDown) {
            return;
        } else {
            event.preventDefault()
            const x = event.clientX
            moved = x - startX
           
            slider.style.left = (scrollLeft + moved) + 'px';
            shifted = moved / slideWidth;
            offset = pixelsToValue(slider.style.left) - slider.parentElement.offsetLeft
            if (shifted - prevShift >= 1) {
                console.log('right one')
                prevShift = shifted;
            } else if (shifted - prevShift <= -1) {
                console.log('left one')
                prevShift = shifted;
            }



        }
    }

}

document.addEventListener("DOMContentLoaded", onLoad);

