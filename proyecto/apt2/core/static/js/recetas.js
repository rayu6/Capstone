function prueba() {
    const modal = new bootstrap.Modal(document.getElementById('agregarIngredienteModal'))
    modal.hide()
    setTimeout(() => {
        // Volver a mostrar el modal con el efecto fade
        modal._element.classList.add('show');
    }, 200);
}

function cambiarLabelsPorInputs() {
    setTimeout(() => {
        console.log(document.getElementById('M_Nombre_Receta'))
        const textarea_ID_Receta = document.getElementById("M_Id");
        const textarea_descripcion = document.getElementById("M_descripcion");
        const textarea_M_Nombre_Receta = document.getElementById("M_Nombre_Receta");

        const label_ID_Receta = document.getElementById("Id_receta");
        const label_ID_descripcion = document.getElementById("Descripcion_Receta");
        const label_ID_nombre = document.getElementById("Nombre_receta");


        $(document).ready(function () {
            // Asocia el evento click a un botón para ocultar el modal
            $('#cerrar').on('click', function () {
                $('.modal.show').modal('hide'); // Cierra el modal
                console.log('prueba')
            });
        });
        if (label_ID_nombre) {
            label_ID_nombre.classList.add('d-none');
        }        
        if (textarea_ID_Receta) {
            textarea_ID_Receta.classList.add('w-100')
        }

        if (textarea_M_Nombre_Receta) {
            textarea_M_Nombre_Receta.classList.remove('d-none');
            textarea_M_Nombre_Receta.classList.add('w-100')
        }
        if (textarea_descripcion) {
            textarea_descripcion.classList.remove('d-none');
            textarea_descripcion.classList.add('w-100');
        }
        const boton_cancelar = document.getElementById("cambiarInputsPorLabels");
        if (boton_cancelar) {
            boton_cancelar.classList.remove('d-none');
        }

        const boton_guardar= document.getElementById("guardar_cambios");
        if (boton_guardar) {
            boton_guardar.classList.remove('d-none');
        }
        

        const boton_modificar= document.getElementById("cambiarLabelsPorInputs");
        if (boton_modificar) {
            boton_modificar.classList.add('d-none');
        }
   }, 150); 
    
}

/*function cambiarLabelsPorInputs() {
    // Mostrar campos de edición y botones
    const textarea_id = document.getElementById('M_Id')
    const textarea_nombre = document.getElementById('M_Nombre_Receta')._element.classList.remove('d-none');
    const textarea_descripcion = document.getElementById('M_descripcion')._element.classList.remove('d-none');
    const boton_cancelar = document.getElementById("cambiarInputsPorLabels");
    //boton_cancelar.style.display="none";
    boton_cancelar._element.classList.add('d-none')

    const boton_guardar= document.getElementById("guardar_cambios");
    if(boton_guardar)
        //boton_guardar.style.display="none";
        boton_guardar._element.classList.add('d-none')
        boton_guardar.style.marginLeft="54.5%";

    const boton_modificar= document.getElementById("cambiarLabelsPorInputs");
    //boton_modificar.style.display="";
    boton_modificar._element.classList.remove('d-none')

}*/

function cambiarInputsPorLabels() {
    

    setTimeout(() => {
        console.log(document.getElementById('M_Nombre_Receta'))
        console.log("si veo esto es que funciono")
        const textarea_ID_Receta = document.getElementById("M_Id");
        const textarea_descripcion = document.getElementById("M_descripcion");
        const textarea_M_Nombre_Receta = document.getElementById("M_Nombre_Receta");
        const label_ID_descripcion = document.getElementById("Descripcion_Receta");
        const label_ID_nombre = document.getElementById("Nombre_receta");

        if (label_ID_descripcion) {
            label_ID_descripcion.classList.remove('d-none');
        }
        if (label_ID_nombre) {
            label_ID_nombre.classList.remove('d-none');
        }
        if (textarea_ID_Receta) {
            textarea_ID_Receta.classList.add('d-none');
        }
        if (textarea_M_Nombre_Receta) {
            textarea_M_Nombre_Receta.classList.add('d-none');
        }
        if (textarea_descripcion) {
            textarea_descripcion.classList.add('d-none');
        }
        const boton_cancelar = document.getElementById("cambiarInputsPorLabels");
        if (boton_cancelar) {
            boton_cancelar.classList.add('d-none');
        }

        const boton_guardar= document.getElementById("guardar_cambios");
        if (boton_guardar) {
            boton_guardar.classList.add('d-none');
        }
        

        const boton_modificar= document.getElementById("cambiarLabelsPorInputs");
        if (boton_modificar) {
            boton_modificar.classList.remove('d-none');
        }
   }, 150);}


if(document.getElementById("cambiarInputsPorLabels")){
    document.getElementById("cambiarInputsPorLabels").addEventListener("click",cerrar );
} 


function cambiarInputsPorLabels() {
    

    setTimeout(() => {
        console.log(document.getElementById('M_Nombre_Receta'))
        console.log("si veo esto es que funciono")
        const textarea_ID_Receta = document.getElementById("M_Id");
        const textarea_descripcion = document.getElementById("M_descripcion");
        const textarea_M_Nombre_Receta = document.getElementById("M_Nombre_Receta");
        const label_ID_descripcion = document.getElementById("Descripcion_Receta");
        const label_ID_nombre = document.getElementById("Nombre_receta");

        if (label_ID_descripcion) {
            label_ID_descripcion.classList.remove('d-none');
        }
        if (label_ID_nombre) {
            label_ID_nombre.classList.remove('d-none');
        }
        if (textarea_ID_Receta) {
            textarea_ID_Receta.classList.add('d-none');
        }
        if (textarea_M_Nombre_Receta) {
            textarea_M_Nombre_Receta.classList.add('d-none');
        }
        if (textarea_descripcion) {
            textarea_descripcion.classList.add('d-none');
        }
        const boton_cancelar = document.getElementById("cambiarInputsPorLabels");
        if (boton_cancelar) {
            boton_cancelar.classList.add('d-none');
        }

        const boton_guardar= document.getElementById("guardar_cambios");
        if (boton_guardar) {
            boton_guardar.classList.add('d-none');
        }
        

        const boton_modificar= document.getElementById("cambiarLabelsPorInputs");
        if (boton_modificar) {
            boton_modificar.classList.remove('d-none');
        }
   }, 150);}


if(document.getElementById("cambiarInputsPorLabels")){
    document.getElementById("cambiarInputsPorLabels").addEventListener("click",cambiarInputsPorLabels );
} 




function Cerrar() {
    
        console.log(document.getElementById('M_Nombre_Receta'))
        console.log("si veo esto es que funciono")
        const textarea_ID_Receta = document.getElementById("M_Id");
        const textarea_descripcion = document.getElementById("M_descripcion");
        const textarea_M_Nombre_Receta = document.getElementById("M_Nombre_Receta");
        const label_ID_descripcion = document.getElementById("Descripcion_Receta");
        const label_ID_nombre = document.getElementById("Nombre_receta");
        const modal_a = document.getElementById("agregarIngredienteModal");
        console.log("prueab de presionado")
        if (modal_a) {
            $('#agregarIngredienteModal').modal('dispose')
           console.log("if modal")

        }
        if (label_ID_descripcion) {
            label_ID_descripcion.classList.remove('d-none');
        }
        if (label_ID_nombre) {
            label_ID_nombre.classList.remove('d-none');
        }
        if (textarea_ID_Receta) {
            textarea_ID_Receta.classList.add('d-none');
        }
        if (textarea_M_Nombre_Receta) {
            textarea_M_Nombre_Receta.classList.add('d-none');
        }
        if (textarea_descripcion) {
            textarea_descripcion.classList.add('d-none');
        }
        const boton_cancelar = document.getElementById("cambiarInputsPorLabels");
        if (boton_cancelar) {
            boton_cancelar.classList.add('d-none');
        }

        const boton_guardar= document.getElementById("guardar_cambios");
        if (boton_guardar) {
            boton_guardar.classList.add('d-none');
        }
        

        const boton_modificar= document.getElementById("cambiarLabelsPorInputs");
        if (boton_modificar) {
            boton_modificar.classList.remove('d-none');
        }
   }


if(document.getElementById("cerrar")){
    document.getElementById("cerrar").addEventListener("click",Cerrar );
    console.log("prueab de presionado")
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

    /* Reset visibility of elements in modal
    document.getElementById('M_Id').style.display = 'none';
    document.getElementById('M_Nombre_Receta').style.display = 'none';
    document.getElementById('M_descripcion').style.display = 'none';
    document.getElementById('guardar_cambios').style.display = 'none';
    document.getElementById('cambiarInputsPorLabels').style.display = 'none';
    document.getElementById('cambiarLabelsPorInputs').style.display = 'block';*/
}
