// Función mejorada para crear pedido
function crearPedido(recetaId) {
    Swal.fire({
        title: '¿Estás seguro?',
        text: 'Confirmar la creación de este pedido',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, crear pedido',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            const tempMods = LocalStorageManager.getModifications(recetaId);
            
            const hasModifications = tempMods && 
                Object.keys(tempMods.modifications).length > 0;
            
            if (typeof pedidosPorUsuarioSocket !== 'undefined') {
                pedidosPorUsuarioSocket.send(JSON.stringify({
                    type: 'nuevo_pedido_modificado',
                    receta_id: recetaId,
                    modifications: hasModifications ? tempMods.modifications : null
                }));
            }

            console.log(hasModifications);
            
            LocalStorageManager.clearModifications(recetaId);
            
            Swal.fire({
                icon: 'success',
                title: '¡Pedido creado!',
                text: 'El pedido se ha creado exitosamente',
                timer: 3000,
                showConfirmButton: false
            }).then(() => {
                window.location.href = '/home/cliente';
            });
        }
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
     if (data.type === 'temp_modification') {
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
    const tempMods = LocalStorageManager.getModifications(recetaId) || { modifications: {} };
    
    // Crear elementos editables para cada ingrediente
    ingredientesOriginales.forEach(ing => {
        const ingredienteId = ing.dataset.ingredienteId;
        const nombre = ing.querySelector('[data-field="ingrediente"]').textContent;
        let cantidad = ing.querySelector('[data-field="cantidad"]').textContent;
        let unidad = ing.querySelector('[data-field="unidad"]').textContent;
        
        // Aplicar modificaciones guardadas si existen
        if (tempMods.modifications[ingredienteId]) {
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
            
            // Obtener modificaciones existentes
            const currentMods = LocalStorageManager.getModifications(recetaId)?.modifications || {};
            
            // Actualizar modificaciones
            currentMods[ingredienteId] = {
                cantidad: newCantidad,
                unidad: newUnidad
            };
            
            // Si no hay mods para un ingrediente, lo agregamos igualmente
            ingredientesOriginales.forEach(originalIng => {
                const originalId = originalIng.dataset.ingredienteId;
                if (!currentMods[originalId]) {
                    currentMods[originalId] = {
                        cantidad: originalIng.querySelector('[data-field="cantidad"]').textContent,
                        unidad: originalIng.querySelector('[data-field="unidad"]').textContent
                    };
                }
            });
            
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
function formatearPrecio(precio) {
    return new Intl.NumberFormat('es-CL').format(precio);
}

// Seleccionar todos los elementos con la clase 'price'
document.addEventListener('DOMContentLoaded', function() {
    const precioElementos = document.querySelectorAll('.price');
    
    precioElementos.forEach(elemento => {
        let precio = parseFloat(elemento.textContent.replace('$', '').trim());
        if (!isNaN(precio)) {
            elemento.textContent = `$${formatearPrecio(precio)}`;
        }
    });
});