document.getElementById('menu-toggle').addEventListener('click', function() {
    const menu = document.getElementById('menu');
    const isExpanded = this.getAttribute('aria-expanded') === 'true';

    // Alternar la visibilidad del menú
    menu.classList.toggle('hidden');
    
    // Actualizar el atributo aria-expanded
    this.setAttribute('aria-expanded', !isExpanded);
});



// script.js

function actualizarStatusNoti(notificationId, status) {
    fetch('/actualizar_status_noti', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrf_token')  // If you are using CSRF protection
        },
        body: `notification_id=${notificationId}&status=${status}`
    }).then(response => {
        if (!response.ok) {
            alert('Error updating notification status');
        }
    });
}

// Obtener el cookie de sesion
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function filterNotifications(filter) {
    const notifications = document.querySelectorAll('.noti-card');
    notifications.forEach(notification => {
        if (filter === 'todo') {
            notification.style.display = 'block';
        } else if (filter === 'leido' && notification.dataset.status === 'leido') {
            notification.style.display = 'block';
        } else if (filter === 'no_leido' && notification.dataset.status === 'no_leido') {
            notification.style.display = 'block';
        } else {
            notification.style.display = 'none';
        }
    });
}