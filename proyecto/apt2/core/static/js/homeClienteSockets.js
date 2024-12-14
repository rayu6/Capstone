const pedidosPorUsuarioSocket = new WebSocket('ws://' + window.location.host + '/ws/pedidos-por-usuario/');
    pedidosPorUsuarioSocket.onopen = function() {
        console.log("Conexión WebSocket establecida para pedidos por usuario.");
    
        pedidosPorUsuarioSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            console.log("WebSocket message received:", data);
        
            if (data.type === 'db_update') {
                handleDatabaseUpdate(data);
            } 
        };

        function handleDatabaseUpdate(data) {
            console.log("Processing DB update for pedido:", data.pedido_id);
            
            const estadoElements = document.querySelectorAll(`.estado-pedido[data-pedido-id="${data.pedido_id}"]`);
            estadoElements.forEach(element => {
                // Determine icon based on estado
                let iconClass = '';
                switch(data.data.estado) {
                    case 'En Proceso':
                        iconClass = 'bi-gear-fill status-icon-proceso';
                        break;
                    case 'Pendiente':
                        iconClass = 'bi-clock-fill status-icon-pendiente';
                        break;
                    case 'Completado':
                        iconClass = 'bi-check-circle-fill text-success';
                        break;
                    case 'Cancelado':
                        iconClass = 'bi-x-circle-fill text-danger';
                        break;
                    default:
                        iconClass = 'bi-question-circle-fill text-secondary';
                }
                
                // Update icon and text
                element.innerHTML = `<i class="bi ${iconClass}"></i> ${data.data.estado}`;
                
                // Add update animation
                element.classList.add('estado-actualizado');
                setTimeout(() => {
                    element.classList.remove('estado-actualizado');
                }, 2000);
            });
        }
        
};