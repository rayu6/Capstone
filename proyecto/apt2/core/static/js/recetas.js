function prueba() {
    const modal = new bootstrap.Modal(document.getElementById('agregarIngredienteModal'))
    modal._element.classList.remove('show');
    setTimeout(() => {
        // Volver a mostrar el modal con el efecto fade
        modal._element.classList.add('show');
    }, 200);
}
document.addEventListener("DOMContentLoaded", function() {
    // Encuentra el botón por su ID
    const boton = document.getElementById("cambiarInputsPorLabels");

    // Agrega un evento 'click' al botón
    boton.addEventListener("click", function() {
        console.log("¡Botón presionado!");
        // Aquí puedes ejecutar tu lógica
        cambiarInputsPorLabels();
    });
});


window.cambiarInputsPorLabels= function () {
    prueba()
    setTimeout(() => {
    document.getElementById('detalle').innerText ='Detalle del Pedido';
    // Cambiar Nombre
    const nameElement = document.getElementById('usuario');
    const nameValue = nameElement.innerText;
    const name2Element = document.getElementById('usuario1');
    const name2Value = name2Element.textContent;


    // Crear un textarea para reemplazar el span
    const nameInput = document.createElement('span');
    nameInput.id = 'usuario';
    nameInput.textContent = name2Value;
    
        const boton_cancelar = document.getElementById("cambiarInputsPorLabels");
        boton_cancelar.style.display="none";

        const boton_guardar= document.getElementById("guardar_cambios");
        boton_guardar.style.display="none";
        boton_guardar.style.marginLeft="54.5%";

        const boton_modificar= document.getElementById("cambiarLabelsPorInputs");
        boton_modificar.style.display="";
    // Reemplazar el span por el textarea
    nameElement.parentNode.replaceChild(nameInput, nameElement);
}, 150); 
     
}

function cambiarLabelsPorInputs() {
    // Mostrar campos de edición y botones
    document.getElementById('M_Id').style.display = 'block';
    document.getElementById('M_Nombre_Receta').style.display = 'block';
    document.getElementById('M_descripcion').style.display = 'block';
    document.getElementById('guardar_cambios').style.display = 'block';
    document.getElementById('cambiarInputsPorLabels').style.display = 'block';
    document.getElementById('cambiarLabelsPorInputs').style.display = 'none';
}

function mostrarId(recetaId) {
    // Busca la tarjeta correspondiente en el DOM
    const recetaCard = document.querySelector(`[data-receta-id="${recetaId}"]`);
    if (!recetaCard) {
        console.error(`Tarjeta con ID ${recetaId} no encontrada.`);
        return;
    }

    // Extrae los valores actualizados del DOM
    const nombre = recetaCard.querySelector('[data-field="nombre_receta"]').textContent.trim();
    const descripcion = recetaCard.querySelector('[data-field="descripcion"]').textContent.trim();

    // Actualiza los valores en el modal
    document.getElementById('Id_receta').textContent = recetaId;
    document.getElementById('M_Id').value = recetaId;
    document.getElementById('Nombre_receta').textContent = nombre;
    document.getElementById('M_Nombre_Receta').value = nombre;
    document.getElementById('Descripcion_Receta').textContent = descripcion;
    document.getElementById('M_descripcion').value = descripcion;

    // Reset visibility of elements in modal
    document.getElementById('M_Id').style.display = 'none';
    document.getElementById('M_Nombre_Receta').style.display = 'none';
    document.getElementById('M_descripcion').style.display = 'none';
    document.getElementById('guardar_cambios').style.display = 'none';
    document.getElementById('cambiarInputsPorLabels').style.display = 'none';
    document.getElementById('cambiarLabelsPorInputs').style.display = 'block';
}
