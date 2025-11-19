window.addEventListener("DOMContentLoaded", onLoad);

// When the DOM content has fully loaded, remember defer
function onLoad() {
  carousel = new Carousel();
  carousel.centerSelected();
}

// Helper function that retrieves the value of a :root defined css variable
function getCssVariable(variable) {
  const root = document.querySelector(":root");
  prop = window.getComputedStyle(root).getPropertyValue(variable);
  return parseInt(prop, 10);
}

// Helper function that retrieves the value of a :root defined css variable
function setCssVariable(variable, value) {
  const root = document.documentElement;
  root.style.setProperty(variable, value);
  return parseInt(prop, 10);
}

// The carousel, and its related code
class Carousel {
	constructor() {
		this.slider = document.querySelector(".slider"); // the slider
		this.slides = this.slider.children; // all the slide elements
		this.isDrag = false; // are we draging
		this.scrollOffset = 0; // keeps track of scroll position relative 0
		this.reference = 0; // used to calculate how far user draged since last move
		this.startX = 0;  // similar to reference, but from initial mouse down
		this.scrollRight = this.slider.scrollWidth - this.slider.offsetWidth; // Right most boundary of slider scroll
		this.velocity = 0; // Used in dragTrail - how fast the user draged
		this.timestamp = 0; // Used for reference timestamp in calculating velocity
		this.frame = 0; // reference pos to calculate distance in velocity tracker
		this.ticker = 0; // dragTrail timer - tracks velocity changes
		this.direction = 0; // -1, 0, 1 to indicate drag direction
		this.timeConstant = 323; // ms - exponential decay rate of dragTrail
		this.selectedCard = document.querySelector(".slide img#active").parentElement;  // card element that is selected
		this.gap = getCssVariable('--gap'); // used for width calculations
		this.element = document.querySelector('.carousel');
		this.isVisible = false;
		this.buttons = document.querySelector('#centered-buttons');

		// calculate slide width
		this.slideWidth = parseInt(this.slides[0].offsetWidth);

		// register events
		window.addEventListener("resize", this.update.bind(this));
		// mouse / desktop drag events
		this.slider.addEventListener("mousedown", this.dragStart.bind(this));
		this.slider.addEventListener("mouseup", this.dragEnd.bind(this));
		this.slider.addEventListener("mousemove", this.dragMove.bind(this));
		this.slider.addEventListener("mouseleave", this.dragEnd.bind(this));
		// touch / mobile drag events
		this.slider.addEventListener("touchstart", this.dragStart.bind(this));
		this.slider.addEventListener("touchmove", this.dragMove.bind(this));
		this.slider.addEventListener("touchend", this.dragEnd.bind(this));
		// set onclick for button #choose-card (toggles visibility)
		const chooseBtn = document.querySelector('#choose-card')
		chooseBtn.addEventListener("click", this.toggleVisibility.bind(this));
		this.update()
		//this.centerSelected();

	}

	// update important properties - called on page resize and during construction
	update() {
		this.slideWidth = this.slides[0].offsetWidth;
		this.slideWidth = parseInt(this.slideWidth, 10);
		this.scrollRight = this.slider.scrollWidth - this.slider.offsetWidth;
		let numberCards = this.slides.length;
		let numberCardsDisplay = getCssVariable('--number-cards')
		let sliderWidth = numberCardsDisplay * this.slideWidth;
		// calculate and set carousel width based on 80% +/- whats needed to fit
		let width = document.body.clientWidth * 0.8
		let ncards = width / this.slideWidth;
		width = Math.round(ncards * this.slideWidth);
		width = width.toString(10) - this.gap + 'px';
		this.slider.scrollLeft = this.gap;  // initial scroll left position
		setCssVariable('--carousel-width', width);
		// save currently selected card number
		let urlPath = window.location.pathname;
		this.selected = urlPath.substring(urlPath.lastIndexOf('/') + 1)
		
	}

	toggleVisibility(event) {
		if (this.isVisible) {
			this.hide();
		} else {
			this.show();
		}

	}

	/* hide carousel : applys hideCarousel animation which changes visibility and height
	*/
	hide() {
		this.isVisible = false;
                this.element.classList.remove('hide')
		this.element.classList.remove('showCarousel')
		this.element.classList.add('hideCarousel')
		this.buttons.style.paddingTop = "72px"
		
	}

	/* show carousel : applys showCarousel animation which changes visibility and height
	*/
	show() {
			this.isVisible = true;
                        this.element.classList.remove('hide')
			this.element.classList.remove('hideCarousel')
			this.element.classList.add('showCarousel')
			this.buttons.style.paddingTop = "0px"

			
	}

	/* centers the carousel on the selected card / slide
	*/
	centerSelected(event) {
		let element = document.querySelector('.slide img#active')
		let scrollMax = this.slider.scrollWidth;
		let offsetLeft = element.offsetLeft - this.slider.offsetLeft;
		let centerView = this.slider.offsetWidth / 2;
		let width =  element.getBoundingClientRect().width;
		let offset = offsetLeft - centerView + width / 2;
		offset = (offset <= 0) ? 0 : (offset >= scrollMax) ? scrollMax : offset
		this.slider.scrollLeft = offset;
		this.scrollOffset = offset;
		console.log('setting ', offset)

	}

	// What to do when draging
	dragMove(event) {
		if (!this.isDrag) return false;
		if (this.isDrag) {
			// make cursor change to grabbing
			this.slider.classList.add('grabbing')
			// Get the mouse or finger X position
			let clientX = this.getClientX(event);
			let moved = this.reference - clientX;
			this.reference = clientX;
			this.direction = (moved > 0) ? 1 : (moved < 0) ? -1 : 0;
			this.scroll(this.direction, this.scrollOffset + moved);
		}

	}

	// Let the dragging begin
	dragStart(event) {
		this.isDrag = true;
		this.slider.classList.remove('snap')
		this.reference = this.getClientX(event);
		this.startX = this.reference;
		this.frame = this.scrollOffset;
		this.timestamp = performance.now();
		clearInterval(this.ticker);
		this.ticker = setInterval(this.trackVelocity.bind(this), 100);
		this.direction = 0;
		event.preventDefault();
		event.stopPropagation();
		return false;
	}

	// make it stop
	dragEnd(event) {
                console.log('dragend')
                console.log('this.startX', this.startX)
                let clientX = this.getClientX(event);
                console.log('clientX', clientX)
		let moved = this.startX - this.getClientX(event);
                console.log('moved', moved)
		// we did not drag, it was a click / select
		if (moved == 0 || isNaN(moved)) {
			let selectedCardNum = event.target.dataset.card;
			let url = window.location.href
			url = url.split('/').slice(0, -1).join('/').concat(`/${selectedCardNum}`)
			if (!selectedCardNum) {
				return false;
			}
			//this.hide()
			window.location.href = url;
			//this.centerSelected(event.target)
		}
		if (!this.isDrag) return false;
		this.isDrag = false;
		this.slider.classList.remove('grabbing')
		clearInterval(this.ticker);
		// Check velocity exceeds threshold
		if (this.velocity > 15 && this.direction == 1 || this.velocity < -15 && this.direction == -1) {
			let amplitude = 0.8 * this.velocity;
			let moveTo = Math.round(this.scrollOffset + amplitude);
			this.timestamp = performance.now();
			requestAnimationFrame(this.dragTrail(amplitude, moveTo));

		}
		event.preventDefault();
		event.stopPropagation();
		return false;
	}

	// Does kenetic or continus drag after release
	dragTrail(amplitude, moveTo) {
		/* Use exponential decay
			https://en.wikipedia.org/wiki/Exponential_decay
		*/
    return () => {
      if (this.isDrag) {
        return false;
      }
      if (amplitude) {
        let elapsed = performance.now() - this.timestamp;
        let delta = -amplitude * Math.exp(-elapsed / this.timeConstant);
        if (delta > 1 || delta < -1) {
          this.scroll(this.direction, moveTo + delta);
          requestAnimationFrame(this.dragTrail(amplitude, moveTo));
        } else {
          this.scroll(this.direction, moveTo);
          this.slider.classList.add("snap");
          this.slider.scrollLeft = this.slider.scrollLeft + 5;
        }
      }
    };
  }

  // Calculates velocity - dx/dt
  trackVelocity() {
    let now = performance.now();
    let elapsed = now - this.timestamp;
    this.timestamp = now;
    let delta = this.scrollOffset - this.frame;
    this.frame = this.scrollOffset;
    let v = (1000 * delta) / (1 + elapsed);
    this.velocity = 0.8 * v + 0.2 * this.velocity;
  }

  // Does the scrolling
  scroll(direction, move) {
    // clamp offset to range (this.scrollLeft <= move <= this.scrollRight)
    this.scrollOffset =
      move >= this.scrollRight ? this.scrollRight : move <= 0 ? 0 : move;

    this.slider.scrollLeft = this.scrollOffset;
    return true;
  }

  // Was this a touch or a mouse event
  getClientX(event) {
    // Is touch event
    if (event.targetTouches) {
      let clientX = event.changedTouches[0].pageX;
      return clientX
    }
    // Desktop - mouse
    return event.clientX;
  }
}
