function reiniciarAnimacionModal(modalElement) {
    // Elimina la clase 'fade' para reiniciar la animación
    modalElement.classList.remove('fade');

    // Forzar el reflow (esto reinicia la animación)
    void modalElement.offsetWidth;

    // Vuelve a añadir la clase 'fade' para que la animación de apertura se aplique
    modalElement.classList.add('fade');
}

function cambiarLabelsPorInputs() {
    const modalElement = document.getElementById('agregarIngredienteModal');
        reiniciarAnimacionModal(modalElement);
    setTimeout(() => {
        console.log(document.getElementById('M_Nombre_Receta'))
        const textarea_ID_Receta = document.getElementById("M_Id");
        const textarea_descripcion = document.getElementById("M_descripcion");
        const textarea_M_Nombre_Receta = document.getElementById("M_Nombre_Receta");

        const label_ID_Receta = document.getElementById("Id_receta");
        const label_ID_descripcion = document.getElementById("Descripcion_Receta");
        const label_ID_nombre = document.getElementById("Nombre_receta");


        if (label_ID_Receta) {
            label_ID_Receta.classList.add('d-none');
        }
        if (label_ID_descripcion) {
            label_ID_descripcion.classList.add('d-none');
        }
        if (label_ID_nombre) {
            label_ID_nombre.classList.add('d-none');
        }
        if (textarea_ID_Receta) {
            textarea_ID_Receta.classList.remove('d-none');
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



function cerrar() {
    

    setTimeout(() => {
        console.log(document.getElementById('M_Nombre_Receta'))
        console.log("si veo esto es que funciono")
        const textarea_ID_Receta = document.getElementById("M_Id");
        const textarea_descripcion = document.getElementById("M_descripcion");
        const textarea_M_Nombre_Receta = document.getElementById("M_Nombre_Receta");



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


