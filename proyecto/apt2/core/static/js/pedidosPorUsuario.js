// Función mejorada para crear pedido
function crearPedido(recetaId) {
    // Obtener modificaciones guardadas
    const tempMods = LocalStorageManager.getModifications(recetaId);
    
    const pedidoData = {
        receta_id: recetaId,
        modificaciones: tempMods ? tempMods.modifications : null
    };
    
    fetch('/api/crear-pedido/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Asegúrate de tener esta función
        },
        body: JSON.stringify(pedidoData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Si tienes WebSocket configurado
            if (typeof pedidosPorUsuarioSocket !== 'undefined') {
                pedidosPorUsuarioSocket.send(JSON.stringify({
                    type: 'nuevo_pedido_modificado',
                    pedido_id: data.pedido_id,
                    receta_id: recetaId,
                    modifications: tempMods ? tempMods.modifications : null
                }));
            }
            
            // Limpiar modificaciones temporales
            LocalStorageManager.clearModifications(recetaId);
            
            toastr.success("¡Pedido creado con éxito!");
        } else {
            toastr.error("Error al crear el pedido");
        }
    })
    .catch(error => {
        console.error('Error:', error);
        toastr.error("Error al procesar el pedido");
    });
}


const pedidosPorUsuarioSocket = new WebSocket('ws://' + window.location.host + '/ws/pedidos-por-usuario/');
    pedidosPorUsuarioSocket.onopen = function() {
        console.log("Conexión WebSocket establecida para pedidos por usuario.");
        console.log("CSRFTOKEN:", getCookie('csrftoken'));  // Verifica el valor de csrftoken
        console.log("SESSIONID:", getCookie('sessionid'));  // Verifica el valor de sessionid
    };

pedidosPorUsuarioSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log("WebSocket message received:", data);

    if (data.type === 'db_update') {
        handleDatabaseUpdate(data);
    } else if (data.type === 'temp_modification') {
        console.log('DB UPDATEEE DATA:' ,data);
        handleTemporaryModification(data);
    }
};

const LocalStorageManager = {
    // Guarda las modificaciones temporales de una receta
    saveModifications: function(recetaId, modifications) {
        const tempData = {
            recetaId,
            modifications,
            timestamp: Date.now()
        };
        localStorage.setItem(`temp_modifications_${recetaId}`, JSON.stringify(tempData));
    },

    // Obtiene las modificaciones guardadas
    getModifications: function(recetaId) {
        const data = localStorage.getItem(`temp_modifications_${recetaId}`);
        return data ? JSON.parse(data) : null;
    },

    // Limpia las modificaciones de una receta
    clearModifications: function(recetaId) {
        localStorage.removeItem(`temp_modifications_${recetaId}`);
    }
};
function mostrarId(recetaId) {
    // Actualizar el ID en el modal
    document.getElementById('Id_receta').textContent = recetaId;
    
    // Obtener la card de la receta
    const recetaCard = document.querySelector(`.card[data-receta-id="${recetaId}"]`);
    
    // Obtener datos de la receta
    const nombre = recetaCard.querySelector('.card-title').textContent;
    const descripcion = recetaCard.querySelector('.dish-description').textContent;
    
    // Actualizar datos en el modal
    document.getElementById('Nombre_receta').textContent = nombre;
    document.getElementById('Descripcion_Receta').textContent = descripcion;
    
    // Obtener y mostrar ingredientes
    const ingredientesContainer = document.getElementById('ingredientes_Receta');
    ingredientesContainer.innerHTML = ''; // Limpiar contenedor
    
    // Obtener lista de ingredientes original
    const ingredientesOriginales = recetaCard.querySelectorAll('.ingrediente-item');
    
    // Obtener modificaciones guardadas
    const tempMods = LocalStorageManager.getModifications(recetaId);
    
    // Crear elementos editables para cada ingrediente
    ingredientesOriginales.forEach(ing => {
        const ingredienteId = ing.dataset.ingredienteId;
        const nombre = ing.querySelector('[data-field="ingrediente"]').textContent;
        let cantidad = ing.querySelector('[data-field="cantidad"]').textContent;
        let unidad = ing.querySelector('[data-field="unidad"]').textContent;
        
        // Aplicar modificaciones guardadas si existen
        if (tempMods && tempMods.modifications[ingredienteId]) {
            cantidad = tempMods.modifications[ingredienteId].cantidad;
            unidad = tempMods.modifications[ingredienteId].unidad;
        }
        
        // Crear elemento editable
        const ingredienteEditable = document.createElement('div');
        ingredienteEditable.className = 'ingrediente-editable mb-2';
        ingredienteEditable.dataset.ingredienteId = ingredienteId;
        ingredienteEditable.innerHTML = `
            <span class="ingrediente-nombre">${nombre}</span>
            <input type="number" class="form-control cantidad-input" value="${cantidad}" min="0" step="0.1">
            <input type="text" class="form-control unidad-input" value="${unidad}">
            <button class="btn btn-sm btn-primary guardar-cambios">Guardar</button>
        `;
        
        ingredientesContainer.appendChild(ingredienteEditable);
        
        // Agregar evento para guardar cambios
        const btnGuardar = ingredienteEditable.querySelector('.guardar-cambios');
        btnGuardar.addEventListener('click', () => {
            const newCantidad = ingredienteEditable.querySelector('.cantidad-input').value;
            const newUnidad = ingredienteEditable.querySelector('.unidad-input').value;
            
            // Obtener modificaciones existentes o crear nuevo objeto
            const currentMods = LocalStorageManager.getModifications(recetaId)?.modifications || {};
            
            // Actualizar modificaciones
            currentMods[ingredienteId] = {
                cantidad: newCantidad,
                unidad: newUnidad
            };
            
            // Guardar en LocalStorage
            LocalStorageManager.saveModifications(recetaId, currentMods);
            
            toastr.success('Cambios guardados temporalmente');
        });
    });
}
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


