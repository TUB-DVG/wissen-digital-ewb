/**
 * Toggle the class of target element via checkbox
*/

const checkboxToggleClass = (() => {

  let checkBox = document.querySelectorAll('[data-checkbox-toggle-class]');
      
  if (checkBox.length === 0) return;
  
  for (let i = 0; i < checkBox.length; i++) {

    checkBox[i].addEventListener('change', function() {
      let target = document.querySelector(this.dataset.bsTarget),
          targetClass = this.dataset.checkboxToggleClass;
      if (this.checked) {
        target.classList.add(targetClass);
      } else {
        target.classList.remove(targetClass);
      }
    });
  }
})();

export default checkboxToggleClass;
