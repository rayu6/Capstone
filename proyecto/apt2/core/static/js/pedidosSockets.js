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
    }
};

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
                // Añadir clase para indicar actualización
                element.classList.add('updated-field');
                setTimeout(() => {
                    element.classList.remove('updated-field');
                }, 2000);
            }
        }
    });
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

function updatePedidoTemp(pedidoId, modifications) {
    const pedidoCard = document.querySelector(`[data-pedido-id="${pedidoId}"]`);
    if (!pedidoCard) return;
    Object.entries(modifications).forEach(([field, value]) => {
        const element = pedidoCard.querySelector(`[data-field="${field}"]`);
        if (element) {
            element.textContent = `${field.charAt(0).toUpperCase() + field.slice(1).replace(/_/g, ' ')}: ${value}`;
        }
    });
}

function actualizarPedido(event) {
    if (event) event.preventDefault();
    
    const pedidoId = document.getElementById('M_Id').value;
    let nuevoEstado = document.getElementById('M_Estado').value;
    
    // Mapear estados descriptivos a IDs si es necesario
    const estadosMap = {
        'En proceso': '1',
        'Pendiente': '2',
        'Completado': '3',
        'Cancelado': '4'
    };
    
    const estadoId = estadosMap[nuevoEstado] || nuevoEstado;
    
    console.log('Enviando actualización:', { pedidoId, nuevoEstado, estadoId });

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
    .then(response => {
        console.log('Response status:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('Server response:', data);
        if (data.status === 'ok') {
            toastr.success("¡Pedido actualizado con éxito!");
            
            // Actualizar UI inmediatamente mientras esperamos la actualización por WebSocket
            const pedidoCard = document.querySelector(`[data-pedido-id="${pedidoId}"]`);
            if (pedidoCard) {
                const estadoElement = pedidoCard.querySelector('[data-field="estado"]');
                if (estadoElement && data.data.estado) {
                    estadoElement.textContent = `Estado: ${data.data.estado}`;
                    estadoElement.dataset.original = data.data.estado;
                }
            }
            
            // Si el modal está abierto, actualizar sus campos también
            const estadoLabel = document.getElementById('Estado_pedido');
            if (estadoLabel) {
                estadoLabel.textContent = data.data.estado;
            }
        } else {
            console.error('Error en la respuesta:', data);
            toastr.error(data.message || "Error al actualizar el pedido");
        }
    })
    .catch(error => {
        console.error('Error en la petición:', error);
        toastr.error("Error al actualizar el pedido");
    });
}

function mostrarId(pedidoId) {
    const pedidoCard = document.querySelector(`[data-pedido-id="${pedidoId}"]`);
    if (!pedidoCard) {
        console.error(`Pedido con ID ${pedidoId} no encontrado`);
        return;
    }

    document.getElementById('pedido').innerText = `Detalles del Pedido ${pedidoId}`;
    document.getElementById('Id_pedido').textContent = pedidoId;
    document.getElementById('M_Id').value = pedidoId;

    const usuario = pedidoCard.querySelector('[data-field="usuario"]').textContent.split(': ')[1];
    document.getElementById('Usuario_pedido').textContent = usuario;
    document.getElementById('M_Usuario').value = usuario;

    const tipoOrden = pedidoCard.querySelector('[data-field="tipo_de_orden"]').textContent.split(': ')[1];
    document.getElementById('Tipo_orden').textContent = tipoOrden;
    document.getElementById('M_Tipo_orden').value = tipoOrden;

    const estado = pedidoCard.querySelector('[data-field="estado"]').textContent.split(': ')[1];
    document.getElementById('Estado_pedido').textContent = estado;
    document.getElementById('M_Estado').value = estado;

    const receta = pedidoCard.querySelector('.card-text:last-child').textContent.split(': ')[1];
    document.getElementById('Receta_pedido').textContent = receta;

    // Reset visibility
    document.getElementById('M_Id').style.display = 'none';
    document.getElementById('M_Usuario').style.display = 'none';
    document.getElementById('M_Tipo_orden').style.display = 'none';
    document.getElementById('M_Estado').style.display = 'none';
    document.getElementById('guardar_cambios').style.display = 'none';
    document.getElementById('cambiarInputsPorLabels').style.display = 'none';
    document.getElementById('cambiarLabelsPorInputs').style.display = 'block';
}

function cambiarLabelsPorInputs() {
    const elementos = {
        'M_Id': 'Id_pedido',
        'M_Usuario': 'Usuario_pedido',
        'M_Tipo_orden': 'Tipo_orden',
        'M_Estado': 'Estado_pedido'
    };

    for (const [input, label] of Object.entries(elementos)) {
        document.getElementById(input).style.display = 'block';
        document.getElementById(label).style.display = 'none';
    }

    document.getElementById('guardar_cambios').style.display = 'block';
    document.getElementById('cambiarInputsPorLabels').style.display = 'block';
    document.getElementById('cambiarLabelsPorInputs').style.display = 'none';
}

function cambiarInputsPorLabels() {
    const elementos = {
        'M_Id': 'Id_pedido',
        'M_Usuario': 'Usuario_pedido',
        'M_Tipo_orden': 'Tipo_orden',
        'M_Estado': 'Estado_pedido'
    };

    for (const [input, label] of Object.entries(elementos)) {
        document.getElementById(input).style.display = 'none';
        document.getElementById(label).style.display = 'block';
    }

    document.getElementById('guardar_cambios').style.display = 'none';
    document.getElementById('cambiarInputsPorLabels').style.display = 'none';
    document.getElementById('cambiarLabelsPorInputs').style.display = 'block';
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
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

    document.querySelectorAll('[contenteditable="true"]').forEach(element => {
        element.addEventListener('input', function() {
            const pedidoCard = this.closest('[data-pedido-id]');
            const pedidoId = pedidoCard.dataset.pedidoId;
            const field = this.dataset.field;
            const value = this.textContent;
            pedidosSocket.send(JSON.stringify({
                action: 'temp_modify',
                pedido_id: pedidoId,
                modifications: { [field]: value }
            }));
        });

        element.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                this.textContent = this.dataset.original;
                e.preventDefault();
            }
        });
    });
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
