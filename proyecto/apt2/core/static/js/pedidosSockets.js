// Configuración del WebSocket
const pedidosSocket = new WebSocket('ws://' + window.location.host + '/ws/pedidos/');
pedidosSocket.onopen = function() {
    console.log("Conexión WebSocket establecida para pedidos.");
};

pedidosSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log("WebSocket message received:", data);

    if (data.type === 'db_update') {
        handleDatabaseUpdate(data);
    } else if (data.type === 'temp_modification') {
        console.log('DB UPDATEEE DATA:' ,data);
        handleTemporaryModification(data);
    } else if (data.type === 'nuevo_pedido') {
        handleNuevoPedido(data.pedido);
        console.log('Nuevo pedido recibido:', data.pedido);
    }
};


function handleNuevoPedido(pedido) {
    console.log(pedido);
    const orderList = document.querySelector('.row');
    if (!orderList) return;
    const pedidoHTML = `
    <div class="col-md-4 mb-4">
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Pedido #${pedido.id}</h5>
            <p><strong>Estado:</strong> ${pedido.estado}</p>
            <p><strong>Tipo de orden:</strong> ${pedido.tipo_de_orden}</p>
            <p><strong>Receta:</strong> ${pedido.receta}</p>
            <p class="card-text" data-field="estado" data-original="${pedido.estado}">Estado: ${pedido.estado}</p>

            <button type="button" class="btn btn-primary" data-bs-toggle="modal" 
                    data-bs-target="#detallePedidoModal" 
                    onclick="fetchDetallePedido(${pedido.id})">
                Ver detalles
            </button>
        </div>
    </div>
    </div>

    `;

    orderList.insertAdjacentHTML('afterbegin', pedidoHTML);

}

function handleDatabaseUpdate(data) {
    console.log("Processing DB update for pedido:", data.pedido_id);
    updatePedidoCard(data.pedido_id, data.data);
    updateModalIfOpen(data.pedido_id, data.data);
}

function handleTemporaryModification(data) {
    console.log("Processing temp modification for pedido:", data);
    updatePedidoCard(data.pedido_id, data.modifications, true);
}

function updatePedidoCard(pedidoId, data, isTemporary = false) {
    const pedidoCard = document.querySelector(`[data-pedido-id="${pedidoId}"]`);
    if (!pedidoCard) return;

    Object.entries(data).forEach(([field, value]) => {
        const element = pedidoCard.querySelector(`[data-field="${field}"]`);
        if (element) {
            const fieldLabel = field.charAt(0).toUpperCase() + field.slice(1).replace(/_/g, ' ');
            element.textContent = `${fieldLabel}: ${value}`;
            
            if (!isTemporary) {
                element.dataset.original = value;
                element.classList.add('updated-field');
                setTimeout(() => {
                    element.classList.remove('updated-field');
                }, 2000);
            }
        }
    });
}

function updateModalIfOpen(pedidoId, data) {
    const modal = document.getElementById('detallePedidoModal');
    const isModalOpen = modal.classList.contains('show');
    
    if (isModalOpen) {
        const currentPedidoId = document.getElementById('pedido_id')?.value;
        if (currentPedidoId === pedidoId.toString()) {
            // Actualizar el estado en el modal si está abierto y es el mismo pedido
            const estadoLabel = document.getElementById('Estado_pedido');
            if (estadoLabel && data.estado) {
                estadoLabel.textContent = data.estado;
            }
        }
    }
}
pedidosSocket.onerror = function(error) {
    console.error("WebSocket error:", error);
};


function updatePedidoFields(pedidoCard, data) {
    if (!pedidoCard) return;
    
    const fields = ['usuario', 'estado', 'tipo_de_orden'];
    fields.forEach(field => {
        const element = pedidoCard.querySelector(`[data-field="${field}"]`);
        if (element && data[field]) {
            element.textContent = `${field.charAt(0).toUpperCase() + field.slice(1).replace(/_/g, ' ')}: ${data[field]}`;
            if (element.hasAttribute('data-original')) {
                element.dataset.original = data[field];
            }
        }
    });
}

function actualizarPedido(event) {
    if (event) event.preventDefault();
    
    const pedidoId = document.getElementById('pedido_id').value;
    let nuevoEstado = document.getElementById('M_Estado').value;
    
    const estadosMap = {
        'En proceso': '1',
        'Pendiente': '2',
        'Completado': '3',
        'Cancelado': '4'
    };
    
    const estadoId = estadosMap[nuevoEstado] || nuevoEstado;
    
    console.log('Enviando actualización:', { pedidoId, nuevoEstado, estadoId });

    // Enviar actualización por WebSocket
    pedidosSocket.send(JSON.stringify({
        action: 'update_estado',
        pedido_id: pedidoId,
        estado: estadoId
    }));

    fetch('/api/update-pedido/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: new URLSearchParams({
            'id': pedidoId,
            'estado': estadoId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'ok') {
            toastr.success("¡Pedido actualizado con éxito!");
            
            // La actualización visual se manejará a través del WebSocket
            cambiarInputsPorLabels();
        } else {
            toastr.error(data.message || "Error al actualizar el pedido");
        }
    })
    .catch(error => {
        console.error('Error en la petición:', error);
        toastr.error("Error al actualizar el pedido");
    });
}

function cambiarLabelsPorInputs() {
    document.getElementById('M_Estado').style.display = 'block';
    document.getElementById('Estado_pedido').style.display = 'none';
    document.getElementById('guardar_cambios').style.display = 'block';
    document.getElementById('cambiarInputsPorLabels').style.display = 'block';
    document.getElementById('cambiarLabelsPorInputs').style.display = 'none';
}

function cambiarInputsPorLabels() {
    document.getElementById('M_Estado').style.display = 'none';
    document.getElementById('Estado_pedido').style.display = 'block';
    document.getElementById('guardar_cambios').style.display = 'none';
    document.getElementById('cambiarInputsPorLabels').style.display = 'none';
    document.getElementById('cambiarLabelsPorInputs').style.display = 'block';
}


function initializeModalEventListeners() {
    const btnModificar = document.getElementById('cambiarLabelsPorInputs');
    if (btnModificar) {
        btnModificar.addEventListener('click', cambiarLabelsPorInputs);
    }

    const btnCancelar = document.getElementById('cambiarInputsPorLabels');
    if (btnCancelar) {
        btnCancelar.addEventListener('click', cambiarInputsPorLabels);
    }

    const btnGuardar = document.getElementById('guardar_cambios');
    if (btnGuardar) {
        btnGuardar.addEventListener('click', actualizarPedido);
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    initializeModalEventListeners();
});
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


function fetchDetallePedido(pedidoId) {
    const url = new URL(window.location.href);
    url.searchParams.set('pedido_id', pedidoId);

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`No se pudo cargar el pedido: ${response.status} ${response.statusText}`);
            }
            return response.text();
        })
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            
            const modalBody = doc.querySelector('#detallePedidoModal .modal-body');
            if (modalBody) {
                document.querySelector('#detallePedidoModal .modal-body').innerHTML = modalBody.innerHTML;
                
                // Reinicializar los event listeners después de actualizar el contenido
                initializeModalEventListeners();
            } else {
                console.error('El contenido del modal no fue encontrado en la respuesta.');
            }
        })
        .catch(err => console.error('Error al cargar detalles del pedido:', err));
}
