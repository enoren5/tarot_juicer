// Change this to control how many cards are visible on carousel at one time
const cardsToDisplay = 5;

function pixelsToInt(pixels) {
    return parseFloat(pixels.substring(0, pixels.length - 2))
}

function onLoad(event) {
    const track = document.querySelector('.carousel_track')
    const slides = Array.from(track.children)
    carousel(track, slides);

}

// Contains all carousel related code, did not use classes for older android support
function carousel(track, slides) {
    let trackWidth;
    let startX;
    let scrollLeft;
    let isDown = false;
    let slideWidth = slides[0].getBoundingClientRect().width;
    const computedTrackWidth = window.getComputedStyle(track).width;
    // const lastCard = slides[slides.length -1];
    // const firstCard = slides[0];
    // const cloneFirst =  firstCard.cloneNode(true);
    // const cloneLast = lastCard.cloneNode(true);
    // slides.push(cloneFirst);
    // slides.unshift(cloneLast);
    // track.appendChild(cloneFirst);
    // track.insertBefore(cloneLast, firstCard)
    slides.forEach((slide, index) => {
        moveAmmount = slideWidth * index + 'px';
        slide.style.left = moveAmmount
    })

    trackWidth = slideWidth * cardsToDisplay;
    track.parentElement.style.width = trackWidth.toString();

    // navigation - events (desktop)
    track.addEventListener('mousedown', dragStart);
    track.addEventListener('mouseup', dragEnd);
    track.addEventListener('mousemove', dragMove);
    track.addEventListener('mouseleave', mouseLeave);
    // navigation - touch events (mobile)
    track.addEventListener('touchstart', dragStart);
    track.addEventListener('touchend', dragEnd);
    track.addEventListener('touchmove', dragMove);

    // handle touch / mouse drag begin
    function dragStart(event) {
        if (event.type.includes('touch')) {
            clientX = event.touches[0].clientX
        } else {
            isDown = true;
            startX = event.clientX;
            scrollLeft = track.scrollLeft;
        }

    }

    // touch / mouse up (drag end)
    function dragEnd(event) {
        isDown = false;
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
            const moved = x - startX
            track.scrollLeft = scrollLeft - moved
            // track.style.left = (scrollLeft - moved) + 'px';
            const cardsShifted = Math.floor(moved / slideWidth)
            console.info(cardsShifted)
            console.info(computedTrackWidth - track.scrolLeft)

            if (cardsShifted >= 1) {
                // take from front, push on back
                // lastCard = slides.pop()
                // slides.unshift(lastCard)
                track.appendChild(track.firstElementChild) 
                

            } else if (cardsShifted <= -1) {
                // take from back push to front
                // first = slides.shift()
                // slides.push(first)

            }
        }
        // clientX = event.type.includes('touch') ? event.touches[0].clientX : event.clientX;
        // posX2 = posX1 - clientX;
        // posX1 = clientX;
        // console.info(`it moved ${posX2}`);
        // track.style.left = `${track.style.left.match(/\d+/g) - posX2}px`;
    }

    function mouseLeave(event) {
        isDown = false;
    }

}

document.addEventListener("DOMContentLoaded", onLoad);

