/**
 * Open YouTube / Vimeo video in lightbox
 * @requires https://github.com/sachinchoolur/lightgallery.js
*/

const videoBtn = (() => {

  let button = document.querySelectorAll('.btn-video');
  if (button.length) {
    for (let i = 0; i < button.length; i++) {
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

})();

export default videoBtn;
