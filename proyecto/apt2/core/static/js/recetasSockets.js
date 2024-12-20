
// Configuración del WebSocket
const recetasSocket = new WebSocket('ws://' + window.location.host + '/ws/recetas/');
recetasSocket.onopen = function() {
    console.log("Conexión WebSocket establecida para recetas.");
};
recetasSocket.onclose = function() {
    console.log("Conexión WebSocket cerrada para recetas.");
};

recetasSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const field = data.field;
    const value = data.value;

    const fieldElement = document.getElementById(field);
    if (fieldElement) {
        fieldElement.textContent = value;
    }
    console.log("WebSocket message received:", data); // Log completo
    console.log("Message type:", data.type);
    console.log("Recipe ID:", data.receta_id);
    console.log("Data:", data.data);
    
    if (data.type === 'db_update') {
        const recetaId = data.receta_id;
        const descripcion = data.data.descripcion;

        console.log(`Receta actualizada: ID ${recetaId}, Nueva descripcion: ${descripcion}`);

        // Actualizar el DOM(el html es el dom)
        const recetaCard = document.querySelector(`[data-receta-id="${recetaId}"]`);
        if (recetaCard) {
            const descripcionElement = recetaCard.querySelector('[data-field="descripcion"]');
            if (descripcionElement) {
                descripcionElement.textContent = descripcion;
                // También actualizar el valor original
                if (descripcionElement.hasAttribute('data-original')) {
                    descripcionElement.dataset.original = descripcion;
                }
            }
        }
    }
     else if (data.type === 'temp_modification') {
        console.log("Attempting temp modification...");
        updateRecetaTemp(data.receta_id, data.modifications);
        console.log("Temp modification completed");
    }
};

function updateRecetaFromDB(recetaId, data) {
    console.log("Updating recipe:", recetaId, data);
    const recetaCard = document.querySelector(`[data-receta-id="${recetaId}"]`);
    if (!recetaCard) {
        console.error("Recipe card not found:", recetaId);
        return;
    }

    // Actualizar cada campo
    Object.entries(data).forEach(([field, value]) => {
        const element = recetaCard.querySelector(`[data-field="${field}"]`);
        if (element) {
            element.textContent = value;
            if (element.hasAttribute('data-original')) {
                element.dataset.original = value;
            }
        }
    });
}

function updateRecetaTemp(recetaId, modifications) {
    const recetaCard = document.querySelector(`[data-receta-id="${recetaId}"]`);
    if (!recetaCard) return;
    Object.entries(modifications).forEach(([field, value]) => {
        const element = recetaCard.querySelector(`[data-field="${field}"]`);
        if (element) {
            element.textContent = value;
        }
    });
}

document.querySelectorAll('[contenteditable="true"]').forEach(element => {
    element.addEventListener('input', function() {
        const recetaCard = this.closest('[data-receta-id]');
        const recetaId = recetaCard.dataset.recetaId;
        const field = this.dataset.field;
        const value = this.textContent;
        recetasSocket.send(JSON.stringify({
            action: 'temp_modify',
            receta_id: recetaId,
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

function actualizarReceta(event) {
    if (event) {
        event.preventDefault();
    }
    
    const recetaId = document.getElementById('M_Id').value;
    const nuevaDescripcion = document.getElementById('M_descripcion').value;
    const nuevoNombre = document.getElementById('M_Nombre_Receta').value;
    const ingredientes = document.querySelectorAll('[id^="nombre_ingrediente-"]');  // Para los ingredientes
    const cantidades = document.querySelectorAll('[id^="input_cantidad-"]');  // Para las cantidades
    const unidades = document.querySelectorAll('[id^="unidad-"]');
    const id_ingrediente = document.querySelectorAll('[id^="ingrediente_id-"]')


    const ingredientesData = [];

    ingredientes.forEach((ingrediente, index) => {
        const ingredienteId = id_ingrediente[index]?.textContent
        const ingredienteValue = ingrediente.textContent || "Sin ingrediente"; // Si no hay ingrediente
        const cantidadValue = cantidades[index]?.value || "Sin cantidad"; // Si no hay cantidad
        const unidadValue = unidades[index]?.textContent || "Sin unidad"; // Si no hay unidad
        
        ingredientesData.push({
            id:ingredienteId,
            ingrediente: ingredienteValue,
            cantidad: cantidadValue,
            unidad: unidadValue
        });
        
    });
    console.log(JSON.stringify(ingredientesData))
    // Obtener el token CSRF
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch('/api/update-receta/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: new URLSearchParams({
            'id': recetaId,
            'descripcion': nuevaDescripcion,
            'nombre_receta': nuevoNombre,
            'ingredientes':JSON.stringify(ingredientesData)
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Respuesta:', data);
        if (data.status === 'ok') {
            toastr.success("¡Receta actualizada con éxito!");

            // Cerrar el modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('agregarIngredienteModal'));
            if (modal) {
                modal.hide();
            }
            
            // Actualizar la vista
            const card = document.querySelector(`[data-receta-id="${recetaId}"]`);
            if (card) {
                // Actualizar descripción
                const descripcionElement = card.querySelector('[data-field="descripcion"]');
                if (descripcionElement) {
                    descripcionElement.textContent = nuevaDescripcion;
                }
                
                // Actualizar nombre
                const nombreElement = card.querySelector('[data-field="nombre_receta"]');
                if (nombreElement) {
                    nombreElement.textContent = nuevoNombre;
                }
            }

        } else {
            console.error('Error en la respuesta:', data.message);
        }
    })
    .catch(error => {
        console.error('Error al actualizar:', error);
    });
}
function recuperar_id(id, div_id,label_id){
    const recetaId = document.getElementById('M_Id').value;
    const div = document.getElementById(div_id)
    const label = document.getElementById(label_id)
    
    
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetch('/api/eliminar_ing_receta/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: new URLSearchParams({
            'id': id
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Respuesta:', data);
        if (data.status === 'ok') {
            toastr.success("¡eliminado con exito!");
            div.remove()
            label.remove()

            // Actualizar la vista
            const card = document.querySelector(`[data-receta-id="${recetaId}"]`);

        } else {
            console.error('Error en la respuesta:', data.message);
        }
    })
    .catch(error => {
        console.error('Error al actualizar:', error);
    });
    
}


// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Event listener para el formulario
    const form = document.getElementById('formActualizarReceta');
    if (form) {
        form.addEventListener('submit', actualizarReceta);
    }

    // Event listener para el botón Modificar
    const btnModificar = document.getElementById('cambiarLabelsPorInputs');
    if (btnModificar) {
        btnModificar.addEventListener('click', cambiarLabelsPorInputs);
    }

    // Event listener para el botón Cancelar
    const btnCancelar = document.getElementById('cambiarInputsPorLabels');
    if (btnCancelar) {
        btnCancelar.addEventListener('click', cambiarInputsPorLabels);
    }

    // Event listeners para campos editables
    document.querySelectorAll('[contenteditable="true"]').forEach(element => {
        element.addEventListener('input', function() {
            const recetaCard = this.closest('[data-receta-id]');
            const recetaId = recetaCard.dataset.recetaId;
            const field = this.dataset.field;
            const value = this.textContent;
            recetasSocket.send(JSON.stringify({
                action: 'temp_modify',
                receta_id: recetaId,
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
