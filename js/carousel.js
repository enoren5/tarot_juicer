
window.addEventListener("DOMContentLoaded", onLoad);

// When the DOM content has fully loaded, remember defer
function onLoad() {
	carousel = new Carousel(document.querySelector(".carousel"));
	carousel.run();
}

// Helper function that retrieves the value of a :root defined css variable
function getCssVariable(variable) {
	const root = document.querySelector(":root");
	prop = window.getComputedStyle(root).getPropertyValue(variable);
	return parseInt(prop, 10);
}

// The carousel, and its related code
class Carousel {
	constructor(carousel) {
		this.slider = document.querySelector(".slider"); // the slider
		this.slides = this.slider.children; // al the slide elements
		this.numberCards = this.slides.length; // total cards before clones
		this.gap = getCssVariable("--gap"); // space between grid cells
		this.isDrag = false; // are we draging
		this.dragPosX = 0; // last drag start position
		this.scrollLeft = 0;  // inital scroll left before drag
		this.dragTimeStart = 0;
		this.moved = 0; // how much it moved, used in calculating velocity

		const indicies = [0, 1, this.numberCards - 2, this.numberCards - 1];
		// get first and last two cards
		let cards = [];
		indicies.forEach(i => cards.push(this.slides[i]));

		// build clones
		let clones = [];
		cards.forEach(card => clones.push(card.cloneNode(true)));

		// inject, append clones to begin / end of slider
		this.slider.insertBefore(clones[clones.length - 1], cards[0]);
		this.slider.insertBefore(
			clones[clones.length - 2],
			this.slider.children[0]
		);
		this.slider.appendChild(clones[0]);
		this.slider.appendChild(clones[1]);

		// calculate slide width and start / end of slider - false start
		this.slideWidth = parseInt(this.slides[0].offsetWidth);
		this.startPos = 2 * (this.slideWidth + this.gap) + this.gap;
		this.endPos = this.slider.scrollWidth - this.startPos;

		// register events
		window.addEventListener("resize", this.update.bind(this));
		this.slider.addEventListener("mousedown", this.dragStart.bind(this));
		this.slider.addEventListener("mouseup", this.dragEnd.bind(this));
		this.slider.addEventListener("mousemove", this.dragMove.bind(this));
		this.slider.addEventListener("mouseleave", this.dragEnd.bind(this));
	}

	// update important properties and more importantly, keep startPos
	update() {
		this.slideWidth = this.slides[0].offsetWidth;

		this.slideWidth = parseInt(this.slideWidth, 10);
		this.startPos = 2 * (this.slideWidth + this.gap) + this.gap;
		this.endPos = this.slider.scrollWidth - this.startPos;

	}

	// Run the carousel, this just ensures the carousel is correctly positioned
	// and is updated with current values of the criticle variables
	run() {
		this.update();

		// scroll to starting position;
		this.slider.scrollLeft = this.startPos;
	}

	// What to do when draging
	dragMove(event) {
		if (!this.isDrag) return false;
		this.moved = event.clientX - this.dragPosX;
		let direction = (this.moved > 0) ? -1 : 1;
		console.log(`Direction ${direction}`);
		this.scroll(direction, this.moved);
	}

	// Let the dragging begin
	dragStart(event) {
		this.isDrag = true;
		this.dragPosX = event.clientX;
		this.scrollLeft = this.slider.scrollLeft;
		this.dragTimeStart = performance.now();
	}

	// make it stop
	dragEnd(event) {
		if (!this.isDrag) return false;
		this.isDrag = false;
		this.direction = 0;
		this.dragTimeEnd = performance.now();
		let deltaX = this.dragTimeEnd - this.dragTimeStart;
		let velocity = parseFloat((this.moved / deltaX).toFixed(2));
		this.dragTrail(this.moved, velocity);
	}

	dragTrail(move, velocity) {
		console.log(`Drag trail ${move} over dropoff ${velocity}`);

	}

	// Checks if user has scrolled past or reached a boundary
	scroll(direction, moved) {
		let toMove = this.scrollLeft - moved;
		let position = this.slider.offsetWidth + toMove;
		if (position >= this.slider.scrollWidth && direction == 1) {
			this.slider.scrollLeft = 0;
			let offset = position - this.slider.scrollWidth;
			this.scrollLeft = 0;
			this.scroll(direction, -offset);
			return true;
		} else if (toMove <= 0 && direction == -1) {
			this.slider.scrollLeft = this.slider.scrollWidth - this.slideWidth;
			if (toMove < 0) {
				this.scrollLeft = this.slider.scrollLeft;
				this.scroll(direction, Math.abs(toMove));
			}
			return true;
		}
		this.slider.scrollLeft = toMove;
	}
}
