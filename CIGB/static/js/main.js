import { Dropdown } from 'flowbite';

function dropmenu(){
    document.getElementById('navbar-default').classList.toggle('hidden')
}

function navbarcenter(){
    const selectedElement = document.querySelector('.selected');
    if (selectedElement) {
        const rect = selectedElement.getBoundingClientRect();
        const contentWidth = document.body.clientWidth;
        
        // Calcular la posición correcta para centrar el scrollbar
        let scrollPosition = rect.left - (contentWidth / 2);
        if (scrollPosition < 0) scrollPosition = 0; // Limitar a cero si está fuera de la pantalla izquierda
        
        document.getElementById('head-menu').scrollTo({
        left: scrollPosition,
        behavior: 'smooth'
        });
    }
}