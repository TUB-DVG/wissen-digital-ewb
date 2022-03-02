/**
 * Content carousel with extensive options to control behaviour and appearance
 * @requires https://github.com/ganlanyuan/tiny-slider
 */


const carousel = (() => {

  // forEach function
  let forEach = function (array, callback, scope) {
    for (let i = 0; i < array.length; i++) {
      callback.call(scope, i, array[i]); // passes back stuff we need
    }
  };
  
  // Carousel initialization
  let carousels = document.querySelectorAll('.tns-carousel-wrapper .tns-carousel-inner');
  forEach(carousels, function (index, value) {
    let defaults = {
      container: value,
      controlsText: ['<i class="ai-arrow-left"></i>', '<i class="ai-arrow-right"></i>'],
      navPosition: 'top',
      controlsPosition: 'top',
      mouseDrag: true,
      speed: 600,
      autoplayHoverPause: true,
      autoplayButtonOutput: false
    };
    let userOptions;
    if(value.dataset.carouselOptions != undefined) userOptions = JSON.parse(value.dataset.carouselOptions);
    let options = {...defaults, ...userOptions};
    let carousel = tns(options);

    let carouselWrapper = value.closest('.tns-carousel-wrapper'),
        carouselItems = carouselWrapper.querySelectorAll('.tns-item');
    
    // Custom pager
    let pager = carouselWrapper.querySelector('.tns-carousel-pager');
    
    if(pager != undefined) {
      
      let pageLinks = pager.querySelectorAll('[data-goto]');

      for (let i = 0; i < pageLinks.length; i++) {
        pageLinks[i].addEventListener('click', function(e) {
          carousel.goTo(this.dataset.goto - 1);
          e.preventDefault();
        });
      }

      carousel.events.on('indexChanged', function() {
        let info = carousel.getInfo();
        for (let n = 0; n < pageLinks.length; n++) {
          pageLinks[n].classList.remove('active');
        }
        pager.querySelector('[data-goto="' + info.displayIndex + '"]').classList.add('active');
      });
    }

    // Change label text
    let labelElem = carouselWrapper.querySelector('.tns-carousel-label');

    if(labelElem != undefined) {
      
      carousel.events.on('indexChanged', function() {
        let info = carousel.getInfo(),
            labelText = carouselItems[info.index].dataset.carouselLabel;

        labelElem.innerHTML = labelText;
      });
    }        
    
    // Progress + slide counter
    if (carouselWrapper.querySelector('.tns-carousel-progress') === null) return;
    
    let carouselInfo = carousel.getInfo(),
        carouselCurrentSlide = carouselWrapper.querySelector('.tns-current-slide'),
        carouselTotalSlides = carouselWrapper.querySelector('.tns-total-slides'),
        carouselProgress = carouselWrapper.querySelector('.tns-carousel-progress .progress-bar');
    
    carouselCurrentSlide.innerHTML = carouselInfo.displayIndex;
    carouselTotalSlides.innerHTML = carouselInfo.slideCount;
    carouselProgress.style.width = (carouselInfo.displayIndex / carouselInfo.slideCount) * 100 + '%';
    
    carousel.events.on('indexChanged', function() {
      let info = carousel.getInfo();
      carouselCurrentSlide.innerHTML = info.displayIndex;
      carouselProgress.style.width = (info.displayIndex / info.slideCount) * 100 + '%';
    });
    
  });
})();

export default carousel;
