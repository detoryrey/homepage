document.addEventListener('DOMContentLoaded', () => {
    const select = document.getElementById('select-history');

    select.addEventListener('change', () => {
        const value = select.value;

        for (let i = 0; i <= 3; i++) {
            const c = document.getElementById('carousel-' + i);
            c.classList.add('d-none');
            c.classList.remove('d-block');
        }
        console.log('Values', value);

        const selectedCarousel = document.getElementById('carousel-' + value);
        selectedCarousel.classList.remove('d-none');
        selectedCarousel.classList.add('d-block');
        console.log();
    });
});