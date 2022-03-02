function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) { symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); } keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(Object(source), true).forEach(function (key) { _defineProperty(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _typeof(obj) { "@babel/helpers - typeof"; if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

/**
 * Around | Multipurpose Bootstrap Template
 * Copyright 2021 Createx Studio
 * Theme core scripts
 * 
 * @author Createx Studio
 * @version 2.4.0
 */
(function () {
  'use strict';
  /**
   * Cascading (Masonry) grid layout
   * 
   * @requires https://github.com/desandro/imagesloaded
   * @requires https://github.com/Vestride/Shuffle
  */

  var masonryGrid = function () {
    var grid = document.querySelectorAll('.masonry-grid'),
        masonry;
    if (grid === null) return;

    var _loop = function _loop(i) {
      masonry = new Shuffle(grid[i], {
        itemSelector: '.masonry-grid-item',
        sizer: '.masonry-grid-item'
      });
      imagesLoaded(grid[i]).on('progress', function () {
        masonry.layout();
      }); // Filtering

      var filtersWrap = grid[i].closest('.masonry-filterable');
      if (filtersWrap === null) return {
        v: void 0
      };
      var filters = filtersWrap.querySelectorAll('.masonry-filters [data-group]');

      for (var n = 0; n < filters.length; n++) {
        filters[n].addEventListener('click', function (e) {
          var current = filtersWrap.querySelector('.masonry-filters .active'),
              target = this.dataset.group;

          if (current !== null) {
            current.classList.remove('active');
          }

          this.classList.add('active');
          masonry.filter(target);
          e.preventDefault();
        });
      }
    };

    for (var i = 0; i < grid.length; i++) {
      var _ret = _loop(i);

      if (_typeof(_ret) === "object") return _ret.v;
    }
  }();
  /**
   * Enable sticky behaviour of navigation bar on page scroll
  */


  var stickyNavbar = function () {
    var navbar = document.querySelector('.navbar-sticky');
    if (navbar == null) return;
    var navbarClass = navbar.classList,
        navbarH = navbar.offsetHeight,
        scrollOffset = 500;

    if (navbarClass.contains('navbar-floating') && navbarClass.contains('navbar-dark')) {
      window.addEventListener('scroll', function (e) {
        if (e.currentTarget.pageYOffset > scrollOffset) {
          navbar.classList.remove('navbar-dark');
          navbar.classList.add('navbar-light', 'navbar-stuck');
        } else {
          navbar.classList.remove('navbar-light', 'navbar-stuck');
          navbar.classList.add('navbar-dark');
        }
      });
    } else if (navbarClass.contains('navbar-floating') && navbarClass.contains('navbar-light')) {
      window.addEventListener('scroll', function (e) {
        if (e.currentTarget.pageYOffset > scrollOffset) {
          navbar.classList.add('navbar-stuck');
        } else {
          navbar.classList.remove('navbar-stuck');
        }
      });
    } else {
      window.addEventListener('scroll', function (e) {
        if (e.currentTarget.pageYOffset > scrollOffset) {
          document.body.style.paddingTop = navbarH + 'px';
          navbar.classList.add('navbar-stuck');
        } else {
          document.body.style.paddingTop = '';
          navbar.classList.remove('navbar-stuck');
        }
      });
    }
  }();
  /**
   * Navbar search toggler
  */


  var navbarSearch = function () {
    var searchTogglers = document.querySelectorAll('[data-bs-toggle="search"]'),
        search = document.querySelector('.navbar-search');
    if (search === null) return;
    var input = search.querySelector('.navbar-search-field');

    for (var i = 0; i < searchTogglers.length; i++) {
      searchTogglers[i].addEventListener('click', function (e) {
        search.classList.toggle('show');
        input.focus();
        e.preventDefault();
      });
    }
  }();
  /**
   * Toggling password visibility in password input
  */


  var passwordVisibilityToggle = function () {
    var elements = document.querySelectorAll('.password-toggle');

    var _loop2 = function _loop2(i) {
      var passInput = elements[i].querySelector('.form-control'),
          passToggle = elements[i].querySelector('.password-toggle-btn');
      passToggle.addEventListener('click', function (e) {
        if (e.target.type !== 'checkbox') return;

        if (e.target.checked) {
          passInput.type = 'text';
        } else {
          passInput.type = 'password';
        }
      }, false);
    };

    for (var i = 0; i < elements.length; i++) {
      _loop2(i);
    }
  }();
  /**
   * Custom file drag and drop area
  */


  var fileDropArea = function () {
    var fileArea = document.querySelectorAll('.file-drop-area');

    var _loop3 = function _loop3(i) {
      var input = fileArea[i].querySelector('.file-drop-input'),
          message = fileArea[i].querySelector('.file-drop-message'),
          icon = fileArea[i].querySelector('.file-drop-icon'),
          button = fileArea[i].querySelector('.file-drop-btn');
      button.addEventListener('click', function () {
        input.click();
      });
      input.addEventListener('change', function () {
        if (input.files && input.files[0]) {
          var reader = new FileReader();

          reader.onload = function (e) {
            var fileData = e.target.result;
            var fileName = input.files[0].name;
            message.innerHTML = fileName;

            if (fileData.startsWith('data:image')) {
              var image = new Image();
              image.src = fileData;

              image.onload = function () {
                icon.className = 'file-drop-preview img-thumbnail rounded';
                icon.innerHTML = '<img src="' + image.src + '" alt="' + fileName + '">';
              };
            } else if (fileData.startsWith('data:video')) {
              icon.innerHTML = '';
              icon.className = '';
              icon.className = 'file-drop-icon ai-film';
            } else {
              icon.innerHTML = '';
              icon.className = '';
              icon.className = 'file-drop-icon ai-file-text';
            }
          };

          reader.readAsDataURL(input.files[0]);
        }
      });
    };

    for (var i = 0; i < fileArea.length; i++) {
      _loop3(i);
    }
  }();
  /**
   * Form validation
  */


  var formValidation = function () {
    var selector = 'needs-validation';
    window.addEventListener('load', function () {
      // Fetch all the forms we want to apply custom Bootstrap validation styles to
      var forms = document.getElementsByClassName(selector); // Loop over them and prevent submission

      var validation = Array.prototype.filter.call(forms, function (form) {
        form.addEventListener('submit', function (e) {
          if (form.checkValidity() === false) {
            e.preventDefault();
            e.stopPropagation();
          }

          form.classList.add('was-validated');
        }, false);
      });
    }, false);
  }();
  /**
   * Input fields formatter
   * @requires https://github.com/nosir/cleave.js
  */


  var inputFormatter = function () {
    var input = document.querySelectorAll('[data-format]');
    if (input.length === 0) return;

    for (var i = 0; i < input.length; i++) {
      var inputFormat = input[i].dataset.format,
          blocks = input[i].dataset.blocks,
          delimiter = input[i].dataset.delimiter;
      blocks = blocks !== undefined ? blocks.split(' ').map(Number) : '';
      delimiter = delimiter !== undefined ? delimiter : ' ';

      switch (inputFormat) {
        case 'card':
          var card = new Cleave(input[i], {
            creditCard: true
          });
          break;

        case 'cvc':
          var cvc = new Cleave(input[i], {
            numeral: true,
            numeralIntegerScale: 3
          });
          break;

        case 'date':
          var date = new Cleave(input[i], {
            date: true,
            datePattern: ['m', 'y']
          });
          break;

        case 'date-long':
          var dateLong = new Cleave(input[i], {
            date: true,
            delimiter: '-',
            datePattern: ['Y', 'm', 'd']
          });
          break;

        case 'time':
          var time = new Cleave(input[i], {
            time: true,
            datePattern: ['h', 'm']
          });
          break;

        case 'custom':
          var custom = new Cleave(input[i], {
            delimiter: delimiter,
            blocks: blocks
          });
          break;

        default:
          console.error('Sorry, your format ' + inputFormat + ' is not available. You can add it to the theme object method - inputFormatter in src/js/theme.js or choose one from the list of available formats: card, cvc, date, date-long, time or custom.');
      }
    }
  }();
  /**
   * Anchor smooth scrolling
   * @requires https://github.com/cferdinandi/smooth-scroll/
  */


  var smoothScroll = function () {
    var selector = '[data-scroll]',
        fixedHeader = '[data-scroll-header]',
        scroll = new SmoothScroll(selector, {
      speed: 800,
      speedAsDuration: true,
      offset: 40,
      header: fixedHeader,
      updateURL: false
    });
  }();
  /**
   * Animate scroll to top button in/off view
  */


  var scrollTopButton = function () {
    var element = document.querySelector('.btn-scroll-top'),
        scrollOffset = 600;
    if (element == null) return;
    var offsetFromTop = parseInt(scrollOffset, 10);
    window.addEventListener('scroll', function (e) {
      if (e.currentTarget.pageYOffset > offsetFromTop) {
        element.classList.add('show');
      } else {
        element.classList.remove('show');
      }
    });
  }();
  /**
   * Tooltip
   * @requires https://getbootstrap.com
   * @requires https://popper.js.org/
  */


  var tooltip = function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl);
    });
  }();
  /**
   * Popover
   * @requires https://getbootstrap.com
   * @requires https://popper.js.org/
  */


  var popover = function () {
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
      return new bootstrap.Popover(popoverTriggerEl);
    });
  }();
  /**
   * Toast
   * @requires https://getbootstrap.com
  */


  var toast = function () {
    var toastElList = [].slice.call(document.querySelectorAll('.toast'));
    var toastList = toastElList.map(function (toastEl) {
      return new bootstrap.Toast(toastEl);
    });
  }();
  /**
   * Lightbox component for presenting various types of media
   * @requires https://github.com/sachinchoolur/lightgallery.js
  */


  var gallery = function () {
    var gallery = document.querySelectorAll('.gallery');

    if (gallery.length) {
      for (var i = 0; i < gallery.length; i++) {
        lightGallery(gallery[i], {
          selector: '.gallery-item',
          download: false,
          videojs: true,
          youtubePlayerParams: {
            modestbranding: 1,
            showinfo: 0,
            rel: 0
          },
          vimeoPlayerParams: {
            byline: 0,
            portrait: 0,
            color: '766df4'
          }
        });
      }
    }
  }();
  /**
   * Ajaxify MailChimp subscription form
  */


  var subscriptionForm = function () {
    var form = document.querySelectorAll('.subscription-form');
    if (form === null) return;

    var _loop4 = function _loop4(i) {
      var button = form[i].querySelector('button[type="submit"]'),
          buttonText = button.innerHTML,
          input = form[i].querySelector('.form-control'),
          antispam = form[i].querySelector('.subscription-form-antispam'),
          status = form[i].querySelector('.subscription-status');
      form[i].addEventListener('submit', function (e) {
        if (e) e.preventDefault();
        if (antispam.value !== '') return;
        register(this, button, input, buttonText, status);
      });
    };

    for (var i = 0; i < form.length; i++) {
      _loop4(i);
    }

    var register = function register(form, button, input, buttonText, status) {
      button.innerHTML = 'Sending...'; // Get url for MailChimp

      var url = form.action.replace('/post?', '/post-json?'); // Add form data to object

      var data = '&' + input.name + '=' + encodeURIComponent(input.value); // Create and add post script to the DOM

      var script = document.createElement('script');
      script.src = url + '&c=callback' + data;
      document.body.appendChild(script); // Callback function

      var callback = 'callback';

      window[callback] = function (response) {
        // Remove post script from the DOM
        delete window[callback];
        document.body.removeChild(script); // Change button text back to initial

        button.innerHTML = buttonText; // Display content and apply styling to response message conditionally

        if (response.result == 'success') {
          input.classList.remove('is-invalid');
          input.classList.add('is-valid');
          status.classList.remove('status-error');
          status.classList.add('status-success');
          status.innerHTML = response.msg;
          setTimeout(function () {
            input.classList.remove('is-valid');
            status.innerHTML = '';
            status.classList.remove('status-success');
          }, 6000);
        } else {
          input.classList.remove('is-valid');
          input.classList.add('is-invalid');
          status.classList.remove('status-success');
          status.classList.add('status-error');
          status.innerHTML = response.msg.substring(4);
          setTimeout(function () {
            input.classList.remove('is-invalid');
            status.innerHTML = '';
            status.classList.remove('status-error');
          }, 6000);
        }
      };
    };
  }();
  /**
   * Updated the text of the label when radio button changes (mainly for color options)
  */


  var labelUpdate = function () {
    var radioBtns = document.querySelectorAll('[data-label]');

    for (var i = 0; i < radioBtns.length; i++) {
      radioBtns[i].addEventListener('change', function () {
        var target = this.dataset.label;

        try {
          document.getElementById(target).textContent = this.value;
        } catch (err) {
          if (err.message = "Cannot set property 'textContent' of null") {
            console.error('Make sure the [data-label] matches with the id of the target element you want to change text of!');
          }
        }
      });
    }
  }();
  /**
   * Content carousel with extensive options to control behaviour and appearance
   * @requires https://github.com/ganlanyuan/tiny-slider
   */


  var carousel = function () {
    // forEach function
    var forEach = function forEach(array, callback, scope) {
      for (var i = 0; i < array.length; i++) {
        callback.call(scope, i, array[i]); // passes back stuff we need
      }
    }; // Carousel initialization


    var carousels = document.querySelectorAll('.tns-carousel-wrapper .tns-carousel-inner');
    forEach(carousels, function (index, value) {
      var defaults = {
        container: value,
        controlsText: ['<i class="ai-arrow-left"></i>', '<i class="ai-arrow-right"></i>'],
        navPosition: 'top',
        controlsPosition: 'top',
        mouseDrag: true,
        speed: 600,
        autoplayHoverPause: true,
        autoplayButtonOutput: false
      };
      var userOptions;
      if (value.dataset.carouselOptions != undefined) userOptions = JSON.parse(value.dataset.carouselOptions);

      var options = _objectSpread(_objectSpread({}, defaults), userOptions);

      var carousel = tns(options);
      var carouselWrapper = value.closest('.tns-carousel-wrapper'),
          carouselItems = carouselWrapper.querySelectorAll('.tns-item'); // Custom pager

      var pager = carouselWrapper.querySelector('.tns-carousel-pager');

      if (pager != undefined) {
        var pageLinks = pager.querySelectorAll('[data-goto]');

        for (var i = 0; i < pageLinks.length; i++) {
          pageLinks[i].addEventListener('click', function (e) {
            carousel.goTo(this.dataset.goto - 1);
            e.preventDefault();
          });
        }

        carousel.events.on('indexChanged', function () {
          var info = carousel.getInfo();

          for (var n = 0; n < pageLinks.length; n++) {
            pageLinks[n].classList.remove('active');
          }

          pager.querySelector('[data-goto="' + info.displayIndex + '"]').classList.add('active');
        });
      } // Change label text


      var labelElem = carouselWrapper.querySelector('.tns-carousel-label');

      if (labelElem != undefined) {
        carousel.events.on('indexChanged', function () {
          var info = carousel.getInfo(),
              labelText = carouselItems[info.index].dataset.carouselLabel;
          labelElem.innerHTML = labelText;
        });
      } // Progress + slide counter


      if (carouselWrapper.querySelector('.tns-carousel-progress') === null) return;
      var carouselInfo = carousel.getInfo(),
          carouselCurrentSlide = carouselWrapper.querySelector('.tns-current-slide'),
          carouselTotalSlides = carouselWrapper.querySelector('.tns-total-slides'),
          carouselProgress = carouselWrapper.querySelector('.tns-carousel-progress .progress-bar');
      carouselCurrentSlide.innerHTML = carouselInfo.displayIndex;
      carouselTotalSlides.innerHTML = carouselInfo.slideCount;
      carouselProgress.style.width = carouselInfo.displayIndex / carouselInfo.slideCount * 100 + '%';
      carousel.events.on('indexChanged', function () {
        var info = carousel.getInfo();
        carouselCurrentSlide.innerHTML = info.displayIndex;
        carouselProgress.style.width = info.displayIndex / info.slideCount * 100 + '%';
      });
    });
  }();
  /**
   * Charts
   * @requires https://github.com/gionkunz/chartist-js
  */


  var charts = function () {
    var lineChart = document.querySelectorAll('[data-line-chart]'),
        barChart = document.querySelectorAll('[data-bar-chart]'),
        pieChart = document.querySelectorAll('[data-pie-chart]');

    var sum = function sum(a, b) {
      return a + b;
    };

    if (lineChart.length === 0 && barChart.length === 0 && pieChart.length === 0) return; // Create <style> tag and put it to <head> for changing colors of charts via data attributes

    var head = document.head || document.getElementsByTagName('head')[0],
        style = document.createElement('style'),
        css;
    head.appendChild(style); // Line chart

    for (var i = 0; i < lineChart.length; i++) {
      var data = JSON.parse(lineChart[i].dataset.lineChart),
          options = lineChart[i].dataset.options != undefined ? JSON.parse(lineChart[i].dataset.options) : '',
          seriesColor = lineChart[i].dataset.seriesColor,
          userColors = void 0;
      lineChart[i].classList.add('line-chart-' + i);

      if (seriesColor != undefined) {
        userColors = JSON.parse(seriesColor);

        for (var n = 0; n < userColors.colors.length; n++) {
          css = "\n          .line-chart-".concat(i, " .ct-series:nth-child(").concat(n + 1, ") .ct-line,\n          .line-chart-").concat(i, " .ct-series:nth-child(").concat(n + 1, ") .ct-point {\n            stroke: ").concat(userColors.colors[n], " !important;\n          }\n        ");
          style.appendChild(document.createTextNode(css));
        }
      }

      new Chartist.Line(lineChart[i], data, options);
    } // Bar chart


    for (var _i = 0; _i < barChart.length; _i++) {
      var _data = JSON.parse(barChart[_i].dataset.barChart),
          _options = barChart[_i].dataset.options != undefined ? JSON.parse(barChart[_i].dataset.options) : '',
          _seriesColor = barChart[_i].dataset.seriesColor,
          _userColors = void 0;

      barChart[_i].classList.add('bar-chart-' + _i);

      if (_seriesColor != undefined) {
        _userColors = JSON.parse(_seriesColor);

        for (var _n = 0; _n < _userColors.colors.length; _n++) {
          css = "\n        .bar-chart-".concat(_i, " .ct-series:nth-child(").concat(_n + 1, ") .ct-bar {\n            stroke: ").concat(_userColors.colors[_n], " !important;\n          }\n        ");
          style.appendChild(document.createTextNode(css));
        }
      }

      new Chartist.Bar(barChart[_i], _data, _options);
    } // Pie chart


    var _loop5 = function _loop5(_i2) {
      var data = JSON.parse(pieChart[_i2].dataset.pieChart),
          seriesColor = pieChart[_i2].dataset.seriesColor,
          userColors = void 0;

      pieChart[_i2].classList.add('cz-pie-chart-' + _i2);

      if (seriesColor != undefined) {
        userColors = JSON.parse(seriesColor);

        for (var _n2 = 0; _n2 < userColors.colors.length; _n2++) {
          css = "\n        .cz-pie-chart-".concat(_i2, " .ct-series:nth-child(").concat(_n2 + 1, ") .ct-slice-pie {\n            fill: ").concat(userColors.colors[_n2], " !important;\n          }\n        ");
          style.appendChild(document.createTextNode(css));
        }
      }

      new Chartist.Pie(pieChart[_i2], data, {
        labelInterpolationFnc: function labelInterpolationFnc(value) {
          return Math.round(value / data.series.reduce(sum) * 100) + '%';
        }
      });
    };

    for (var _i2 = 0; _i2 < pieChart.length; _i2++) {
      _loop5(_i2);
    }
  }();
  /**
   * Countdown timer
  */


  var countdown = function () {
    var coundown = document.querySelectorAll('.countdown');
    if (coundown == null) return;

    var _loop6 = function _loop6(i) {
      var endDate = coundown[i].dataset.countdown,
          daysVal = coundown[i].querySelector('.countdown-days .countdown-value'),
          hoursVal = coundown[i].querySelector('.countdown-hours .countdown-value'),
          minutesVal = coundown[i].querySelector('.countdown-minutes .countdown-value'),
          secondsVal = coundown[i].querySelector('.countdown-seconds .countdown-value'),
          days = void 0,
          hours = void 0,
          minutes = void 0,
          seconds = void 0;
      endDate = new Date(endDate).getTime();
      if (isNaN(endDate)) return {
        v: void 0
      };
      setInterval(calculate, 1000);

      function calculate() {
        var startDate = new Date().getTime();
        var timeRemaining = parseInt((endDate - startDate) / 1000);

        if (timeRemaining >= 0) {
          days = parseInt(timeRemaining / 86400);
          timeRemaining = timeRemaining % 86400;
          hours = parseInt(timeRemaining / 3600);
          timeRemaining = timeRemaining % 3600;
          minutes = parseInt(timeRemaining / 60);
          timeRemaining = timeRemaining % 60;
          seconds = parseInt(timeRemaining);

          if (daysVal != null) {
            daysVal.innerHTML = parseInt(days, 10);
          }

          if (hoursVal != null) {
            hoursVal.innerHTML = hours < 10 ? '0' + hours : hours;
          }

          if (minutesVal != null) {
            minutesVal.innerHTML = minutes < 10 ? '0' + minutes : minutes;
          }

          if (secondsVal != null) {
            secondsVal.innerHTML = seconds < 10 ? '0' + seconds : seconds;
          }
        } else {
          return;
        }
      }
    };

    for (var i = 0; i < coundown.length; i++) {
      var _ret2 = _loop6(i);

      if (_typeof(_ret2) === "object") return _ret2.v;
    }
  }();
  /**
   * Date / time picker
   * @requires https://github.com/flatpickr/flatpickr
   */


  var datePicker = function () {
    var picker = document.querySelectorAll('.date-picker');
    if (picker.length === 0) return;

    for (var i = 0; i < picker.length; i++) {
      var defaults = {
        disableMobile: 'true'
      };
      var userOptions = void 0;
      if (picker[i].dataset.datepickerOptions != undefined) userOptions = JSON.parse(picker[i].dataset.datepickerOptions);
      var linkedInput = picker[i].classList.contains('date-range') ? {
        "plugins": [new rangePlugin({
          input: picker[i].dataset.linkedInput
        })]
      } : '{}';

      var options = _objectSpread(_objectSpread(_objectSpread({}, defaults), linkedInput), userOptions);

      flatpickr(picker[i], options);
    }
  }();
  /**
   * Change tabs with radio buttons
   * @method radioTabs
  */


  var radioTab = function () {
    var radioBtns = document.querySelectorAll('[data-bs-toggle="radioTab"]');

    for (var i = 0; i < radioBtns.length; i++) {
      radioBtns[i].addEventListener('click', function () {
        var target = this.dataset.bsTarget,
            parent = document.querySelector(this.dataset.bsParent),
            children = parent.querySelectorAll('.radio-tab-pane');
        children.forEach(function (element) {
          element.classList.remove('active');
        });
        document.querySelector(target).classList.add('active');
      });
    }
  }();
  /**
   * Mouse move parallax effect
   * @requires https://github.com/wagerfield/parallax
  */


  var parallax = function () {
    var element = document.querySelectorAll('.parallax');

    for (var i = 0; i < element.length; i++) {
      var parallaxInstance = new Parallax(element[i]);
    }
  }();
  /**
   * Switch price inside pricing plans
  */


  var priceSwitch = function () {
    var pricing = document.querySelectorAll('.pricing-wrap');
    if (pricing === null) return;

    var _loop7 = function _loop7(i) {
      var priceSwitch = pricing[i].querySelector('.form-switch'),
          priceSwitchInput = priceSwitch.querySelector('input[type="checkbox"]'),
          priceElement = pricing[i].querySelectorAll('.price');

      var changeState = function changeState() {
        if (priceSwitchInput.checked) {
          priceSwitch.parentNode.classList.add('price-switch-on');

          for (var n = 0; n < priceElement.length; n++) {
            priceElement[n].innerHTML = priceElement[n].dataset.newPrice;
          }
        } else {
          priceSwitch.parentNode.classList.remove('price-switch-on');

          for (var m = 0; m < priceElement.length; m++) {
            priceElement[m].innerHTML = priceElement[m].dataset.currentPrice;
          }
        }
      };

      changeState();
      priceSwitchInput.addEventListener('change', function () {
        changeState();
      });
    };

    for (var i = 0; i < pricing.length; i++) {
      _loop7(i);
    }
  }();
  /**
   * Shop product page gallery with thumbnails
  */


  var productGallery = function () {
    var gallery = document.querySelectorAll('.product-gallery');

    if (gallery.length) {
      var _loop8 = function _loop8(i) {
        var thumbnails = gallery[i].querySelectorAll('.product-gallery-thumblist-item'),
            previews = gallery[i].querySelectorAll('.product-gallery-preview-item');

        for (var n = 0; n < thumbnails.length; n++) {
          thumbnails[n].addEventListener('click', changePreview);
        } // Changer preview function


        function changePreview(e) {
          e.preventDefault();

          for (var _i3 = 0; _i3 < thumbnails.length; _i3++) {
            previews[_i3].classList.remove('active');

            thumbnails[_i3].classList.remove('active');
          }

          this.classList.add('active');
          gallery[i].querySelector(this.getAttribute('href')).classList.add('active');
        }
      };

      for (var i = 0; i < gallery.length; i++) {
        _loop8(i);
      }
    }
  }();
  /**
   * Open YouTube / Vimeo video in lightbox
   * @requires https://github.com/sachinchoolur/lightgallery.js
  */


  var videoBtn = function () {
    var button = document.querySelectorAll('.btn-video');

    if (button.length) {
      for (var i = 0; i < button.length; i++) {
        lightGallery(button[i], {
          selector: 'this',
          download: false,
          videojs: true,
          youtubePlayerParams: {
            modestbranding: 1,
            showinfo: 0,
            rel: 0
          },
          vimeoPlayerParams: {
            byline: 0,
            portrait: 0,
            color: '766df4'
          }
        });
      }
    }
  }();
  /**
   * Range slider
   * @requires https://github.com/leongersen/noUiSlider
  */


  var rangeSlider = function () {
    var rangeSliderWidget = document.querySelectorAll('.range-slider');

    var _loop9 = function _loop9(i) {
      var rangeSlider = rangeSliderWidget[i].querySelector('.range-slider-ui'),
          valueMinInput = rangeSliderWidget[i].querySelector('.range-slider-value-min'),
          valueMaxInput = rangeSliderWidget[i].querySelector('.range-slider-value-max');
      var options = {
        dataStartMin: parseInt(rangeSliderWidget[i].dataset.startMin, 10),
        dataStartMax: parseInt(rangeSliderWidget[i].dataset.startMax, 10),
        dataMin: parseInt(rangeSliderWidget[i].dataset.min, 10),
        dataMax: parseInt(rangeSliderWidget[i].dataset.max, 10),
        dataStep: parseInt(rangeSliderWidget[i].dataset.step, 10)
      };
      noUiSlider.create(rangeSlider, {
        start: [options.dataStartMin, options.dataStartMax],
        connect: true,
        step: options.dataStep,
        pips: {
          mode: 'count',
          values: 5
        },
        tooltips: true,
        range: {
          'min': options.dataMin,
          'max': options.dataMax
        },
        format: {
          to: function to(value) {
            return '$' + parseInt(value, 10);
          },
          from: function from(value) {
            return Number(value);
          }
        }
      });
      rangeSlider.noUiSlider.on('update', function (values, handle) {
        var value = values[handle];
        value = value.replace(/\D/g, '');

        if (handle) {
          valueMaxInput.value = Math.round(value);
        } else {
          valueMinInput.value = Math.round(value);
        }
      });
      valueMinInput.addEventListener('change', function () {
        rangeSlider.noUiSlider.set([this.value, null]);
      });
      valueMaxInput.addEventListener('change', function () {
        rangeSlider.noUiSlider.set([null, this.value]);
      });
    };

    for (var i = 0; i < rangeSliderWidget.length; i++) {
      _loop9(i);
    }
  }();
  /**
   * View switcher
  */


  var viewSwitcher = function () {
    var switcher = document.querySelectorAll('[data-view]');

    if (switcher.length > 0) {
      for (var i = 0; i < switcher.length; i++) {
        switcher[i].addEventListener('click', function (e) {
          var target = this.dataset.view;
          viewSwitch(target);
          if (this.getAttribute('href') === '#') e.preventDefault();
        });
      }
    }

    var viewSwitch = function viewSwitch(target) {
      var targetView = document.querySelector(target),
          targetParent = targetView.parentNode,
          siblingViews = targetParent.querySelectorAll('.view');

      for (var n = 0; n < siblingViews.length; n++) {
        siblingViews[n].classList.remove('show');
      }

      targetView.classList.add('show');
    };
  }();
  /**
   * Toggle the class of target element via checkbox
  */


  var checkboxToggleClass = function () {
    var checkBox = document.querySelectorAll('[data-checkbox-toggle-class]');
    if (checkBox.length === 0) return;

    for (var i = 0; i < checkBox.length; i++) {
      checkBox[i].addEventListener('change', function () {
        var target = document.querySelector(this.dataset.bsTarget),
            targetClass = this.dataset.checkboxToggleClass;

        if (this.checked) {
          target.classList.add(targetClass);
        } else {
          target.classList.remove(targetClass);
        }
      });
    }
  }();
  /**
   * Master checkbox that checkes / unchecks all target checkboxes at once
  */


  var masterCheckbox = function () {
    var masterCheckbox = document.querySelectorAll('[data-master-checkbox-for]');
    if (masterCheckbox.length === 0) return;

    for (var i = 0; i < masterCheckbox.length; i++) {
      masterCheckbox[i].addEventListener('change', function () {
        var targetWrapper = document.querySelector(this.dataset.masterCheckboxFor),
            targetCheckboxes = targetWrapper.querySelectorAll('input[type="checkbox"]');

        if (this.checked) {
          for (var n = 0; n < targetCheckboxes.length; n++) {
            targetCheckboxes[n].checked = true;

            if (targetCheckboxes[n].dataset.checkboxToggleClass) {
              document.querySelector(targetCheckboxes[n].dataset.bsTarget).classList.add(targetCheckboxes[n].dataset.checkboxToggleClass);
            }
          }
        } else {
          for (var m = 0; m < targetCheckboxes.length; m++) {
            targetCheckboxes[m].checked = false;

            if (targetCheckboxes[m].dataset.checkboxToggleClass) {
              document.querySelector(targetCheckboxes[m].dataset.bsTarget).classList.remove(targetCheckboxes[m].dataset.checkboxToggleClass);
            }
          }
        }
      });
    }
  }();
})();