const offcanvasElementList = document.querySelectorAll('.offcanvas')
const closeOffCanvas = document.getElementById('offcanvasDarkClose');
const body = document.querySelectorAll('body');

closeOffCanvas.addEventListener('click', () => {
    offcanvasElementList[0].classList.remove('show')
    body[0].classList.add('opacity-100')
});
