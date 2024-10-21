document.getElementById('menu-toggle').addEventListener('click', function() {
    const menu = document.getElementById('menu');
    const isExpanded = this.getAttribute('aria-expanded') === 'true';

    // Alternar la visibilidad del menú
    menu.classList.toggle('hidden');
    
    // Actualizar el atributo aria-expanded
    this.setAttribute('aria-expanded', !isExpanded);
});
