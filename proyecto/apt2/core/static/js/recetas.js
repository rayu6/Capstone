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
            });
        });
        if (label_ID_nombre) {
            label_ID_nombre.classList.add('d-none');
        }        
        if (textarea_ID_Receta) {
            textarea_ID_Receta.classList.add('w-100')
        }

        if (label_ID_descripcion) {
            label_ID_descripcion.classList.add('d-none')
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

        const label_cantidad = document.querySelectorAll('[id^="cantidad-"]')
        
        label_cantidad.forEach((cantidad) => {
            // Agrega la clase 'd-none' para ocultar el elemento
            cantidad.classList.add('d-none');
            
        });

        const label_unidades = document.querySelectorAll('[id^="unidad-"]')
        
        label_unidades.forEach((unidad) => {
            // Agrega la clase 'd-none' para ocultar el elemento
            unidad.classList.add('d-none');
        });


        const div_input = document.querySelectorAll('[id^="inputs_ingredientes-"]')
        
        div_input.forEach((div_input) => {
            // Agrega la clase 'd-none' para ocultar el elemento
            div_input.classList.remove('d-none');
        });


        const input_cantidades =document.querySelectorAll('[id^="input_cantidad-"]');
        input_cantidades.forEach((cantidad) => {
            const cantidadValue = cantidad.value  ; 
            console.log(cantidadValue);})
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

        const label_cantidad = document.querySelectorAll('[id^="cantidad-"]')
        
        label_cantidad.forEach((cantidad) => {
            
            // Agrega la clase 'd-none' para ocultar el elemento
            cantidad.classList.remove('d-none');
            
        });

        const label_unidades = document.querySelectorAll('[id^="unidad-"]')
        
        label_unidades.forEach((unidad) => {
            // Agrega la clase 'd-none' para ocultar el elemento
            unidad.classList.remove('d-none');
        });


        const div_input = document.querySelectorAll('[id^="inputs_ingredientes-"]')
        
        div_input.forEach((div_input) => {
            // Agrega la clase 'd-none' para ocultar el elemento
            div_input.classList.add('d-none');
        });
   }, 150);}


if(document.getElementById("cambiarInputsPorLabels")){
    document.getElementById("cambiarInputsPorLabels").addEventListener("click",cambiarInputsPorLabels );
} 




function Cerrar() {
    setTimeout(() => {
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
        const label_cantidad = document.querySelectorAll('[id^="cantidad-"]')
        
        label_cantidad.forEach((cantidad) => {
            
            // Agrega la clase 'd-none' para ocultar el elemento
            cantidad.classList.remove('d-none');
            
        });

        const label_unidades = document.querySelectorAll('[id^="unidad-"]')
        
        label_unidades.forEach((unidad) => {
            // Agrega la clase 'd-none' para ocultar el elemento
            unidad.classList.remove('d-none');
        });


        const div_input = document.querySelectorAll('[id^="inputs_ingredientes-"]')
        
        div_input.forEach((div_input) => {
            // Agrega la clase 'd-none' para ocultar el elemento
            div_input.classList.add('d-none');
        });
   }
, 150);}

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
    const ingredientes = recetaCard.querySelectorAll('[data-field="ingrediente"]');
    const cantidades =recetaCard.querySelectorAll('[data-field="cantidad"]');
    const unidades =recetaCard.querySelectorAll('[data-field="unidad"]');
    const id_ingrediente = recetaCard.querySelectorAll('[data-field="id-ingrediente"]');
     // Recopila los ingredientes

    const contenedor = document.getElementById('ingredientes_Receta'); // Selecciona el contenedor
    contenedor.innerHTML=''
        

    
    ingredientes.forEach((ingrediente, index) => {
        const id = id_ingrediente[index]?.textContent
        const nombre = ingrediente.textContent.trim();
        const cantidad = cantidades[index]?.textContent.trim() || "Sin cantidad";
        const unidad = unidades[index]?.textContent.trim() || "Sin unidad";
        const contenedorIngrediente = document.createElement('div');

        console.log(id)
    
        // Agrega nombre

        const label_id_Ingrediente = document.createElement('label');
            label_id_Ingrediente.id=`ingrediente_id-${index+1}`;
            label_id_Ingrediente.classList.add('d-none');
            label_id_Ingrediente.textContent=id;
        contenedorIngrediente.appendChild(label_id_Ingrediente)

        const labelIngrediente = document.createElement('label');
        labelIngrediente.textContent = nombre;
        labelIngrediente.id=`nombre_ingrediente-${index+1}`
        contenedorIngrediente.appendChild(labelIngrediente);
    
        // Agrega cantidad
        const labelCantidad = document.createElement('label');
        labelCantidad.innerHTML = `&nbsp;${cantidad} `;
        labelCantidad.id=`cantidad-${index+1}`
        contenedorIngrediente.appendChild(labelCantidad);
    
        // Agrega unidad
        const labelUnidad = document.createElement('label');
        labelUnidad.innerHTML= `&nbsp;${unidad} `;
        labelUnidad.id=`unidad-${index+1}`
        contenedorIngrediente.appendChild(labelUnidad);
        

        //CREACION INPUTS
        const div_inputs = document.createElement('div');
            div_inputs.id=`inputs_ingredientes-${index+1}`;

            div_inputs.classList.add('d-none');

            div_inputs.classList.add('input-group');
            //span cantidades
            const span_c = document.createElement('span');
                span_c.classList.add('input-group-text');
                span_c.id=`span_cantidad-${index+1}`;
                span_c.textContent= "cantidad";
                div_inputs.appendChild(span_c);

            const input_c = document.createElement('input');
                input_c.classList.add('form-control');
                input_c.id=`input_cantidad-${index+1}`;
                input_c.value= cantidad;
                div_inputs.appendChild(input_c);
            
            const span_u = document.createElement('span');
                span_u.classList.add('input-group-text');
                span_c.id=`span_unidad-${index+1}`;
                span_u.textContent= "unidad";
                div_inputs.appendChild(span_u);

            const input_u = document.createElement('input');
                input_u.classList.add('form-control');
                input_c.id=`input_cantidad-${index+1}`;
                input_u.value= unidad;
                div_inputs.appendChild(input_u);

        // Añadir al DOM
        contenedor.appendChild(contenedorIngrediente);
        contenedor.appendChild(div_inputs);
    });

    const textarea_descripcion = document.getElementById("M_descripcion");
    const textarea_M_Nombre_Receta = document.getElementById("M_Nombre_Receta");

    textarea_M_Nombre_Receta.classList.add('d-none');
    textarea_descripcion.classList.add('d-none')

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

        const label_ID_descripcion = document.getElementById("Descripcion_Receta");
        const label_ID_nombre = document.getElementById("Nombre_receta");

        label_ID_descripcion.classList.remove('d-none')
        label_ID_nombre.classList.remove('d-none')

    
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
