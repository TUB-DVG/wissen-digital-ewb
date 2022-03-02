/**
 * Navbar search toggler
*/

const navbarSearch = (() => {

  let searchTogglers = document.querySelectorAll('[data-bs-toggle="search"]'),
  search = document.querySelector('.navbar-search');

  if (search === null) return;

  let input = search.querySelector('.navbar-search-field');

  for (let i = 0; i < searchTogglers.length; i++) {
    searchTogglers[i].addEventListener('click', (e) => {
      search.classList.toggle('show');
      input.focus();
      e.preventDefault();
    });
  }

})();

export default navbarSearch;
