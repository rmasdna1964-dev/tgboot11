const links = document.querySelectorAll('.nav-link');
const light = document.querySelector('.nav-light');

function activeLink(linkActive) {
    links.forEach(link => {
        link.classList.remove('active');
    });
    linkActive.classList.add('active');
}

links.forEach((item, index) => {
    item.addEventListener('click', (e) => {
        e.preventDefault();
        activeLink(item);
        
        // Смещение белой плашки-индикатора при клике
        // 70px — это примерный шаг для каждой иконки, подстройте под ваш CSS если нужно
        light.style.transform = `translateX(${index * 70}px)`;
    });
});
