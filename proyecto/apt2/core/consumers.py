import json
from venv import logger
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.shortcuts import get_object_or_404
from .models import Recetas, RecetaIngrediente, Usuario
from django.apps import apps

class RecetasConsumer(AsyncWebsocketConsumer):
    _temp_modifications = {}  # Diccionario para almacenar modificaciones temporales

    async def connect(self):
        await self.channel_layer.group_add("recetas_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("recetas_group", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        
        if action == 'temp_modify':
            # Maneja modificaciones temporales
            receta_id = data.get('receta_id')
            modifications = data.get('modifications')
            
            # Almacena las modificaciones temporales
            self._temp_modifications[receta_id] = modifications
            
            # Transmite las modificaciones a todos los clientes
            await self.channel_layer.group_send(
                "recetas_group",
                {
                    "type": "broadcast_temp_modification",
                    "receta_id": receta_id,
                    "modifications": modifications
                }
            )

    async def broadcast_temp_modification(self, event):
        await self.send(text_data=json.dumps({
            'type': 'temp_modification',
            'receta_id': event['receta_id'],
            'modifications': event['modifications']
        }))

    async def broadcast_db_update(self, event):
        print(f"📨 Processing broadcast_db_update: {event}")
        try:
            message = {
                'type': 'db_update',
                'receta_id': event['receta_id'],
                'data': event['data']
            }
            print(f"📝 Preparing message: {message}")
            await self.send(text_data=json.dumps(message))
            print("✅ Message sent to client successfully")
        except Exception as e:
            print(f"❌ Error in broadcast_db_update: {str(e)}")
            import traceback
            print(traceback.format_exc())


class PedidosPorUsuarioConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.processed_uuids = set()  # Aquí almacenaremos los UUIDs procesados

    async def connect(self):
        # Usamos solo este grupo
        await self.channel_layer.group_add("pedidos_por_usuario_group", self.channel_name)
        self.usuario = await self.get_usuario(1)
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("pedidos_por_usuario_group", self.channel_name)
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        uuid = data.get('uuid')

        # Validar UUID y evitar procesarlo más de una vez
        if uuid and uuid in self.processed_uuids:
            await self.send(json.dumps({"error": "UUID ya procesado"}))
            return
        elif uuid:
            self.processed_uuids.add(uuid)

        if data.get('type') == 'nuevo_pedido_modificado':
            # Crear el pedido en la base de datos
            pedido_creado = await self.crear_pedido(
                data['receta_id'],
                data.get('modifications', None)
            )
            
            if pedido_creado:
                # Enviamos solo una vez al grupo
                await self.channel_layer.group_send(
                    "pedidos_por_usuario_group",
                    {
                        "type": "nuevo_pedido_mensaje",
                        "pedido": await self.serializar_pedido(pedido_creado),
                        "uuid": uuid,  # Añadimos el UUID al evento
                        }
                    )
        if data.get('action') == 'update_estado':
            pedido_id = data.get('pedido_id')
            estado = data.get('estado')

            updated_pedido = await self.actualizar_estado_pedido(pedido_id, estado)
            
            if updated_pedido:
                await self.channel_layer.group_send(
                    "pedidos_por_usuario_group",
                    {
                        "type": "update_pedido_estado",
                        "pedido_id": pedido_id,
                        "data": {
                            "estado": str(updated_pedido.estado)
                        }
                    }
                )

    async def nuevo_pedido_mensaje(self, event):
        # Enviamos el mensaje una sola vez
        await self.send(text_data=json.dumps({
            'type': 'nuevo_pedido',
            'pedido': event['pedido'],
            'uuid': event['uuid'],  # Incluir el UUID en la respuesta

        }))

    async def update_pedido_estado(self, event):
        await self.send(text_data=json.dumps({
            'type': 'db_update',
            'pedido_id': event['pedido_id'],
            'data': event['data']
        }))

    @database_sync_to_async
    def actualizar_estado_pedido(self, pedido_id, new_estado_id):
        try:
            Pedido = apps.get_model('core', 'Pedido')
            Estado = apps.get_model('core', 'Estado')

            pedido = Pedido.objects.get(id=pedido_id)
            pedido.estado = Estado.objects.get(id=new_estado_id)
            pedido.save()
            
            return pedido
        except Exception as e:
            print(f"Error al actualizar estado del pedido: {str(e)}")
            return None
        
    @database_sync_to_async
    def get_usuario(self, usuario_id):
        return get_object_or_404(Usuario, id=usuario_id)
    
    @database_sync_to_async
    def crear_pedido(self, receta_id, modifications=None):
        try:
            # Obtener modelos
            Pedido = apps.get_model('core', 'Pedido')
            RecetaPedido = apps.get_model('core', 'RecetaPedido')
            Recetas = apps.get_model('core', 'Recetas')
            Estado = apps.get_model('core', 'Estado')
            TipoDeOrden = apps.get_model('core', 'TipoDeOrden')
            RecetaModificada = apps.get_model('core', 'RecetaModificada')
            RecetaIngrediente = apps.get_model('core', 'RecetaIngrediente')

            # Obtener receta original
            receta = Recetas.objects.get(id=receta_id)
            receta_pedido = RecetaPedido.objects.create(recetas=receta)

            # Inicializar receta modificada como None
            receta_modificada = None

            # Si hay modificaciones, crear RecetaModificada
            if modifications:
                receta_modificada = RecetaModificada.objects.create(
                    receta_original=receta,
                    usuario=self.usuario
                )

                # Añadir ingredientes modificados
                for ing_id, cambios in modifications.items():
                    ingrediente_original = RecetaIngrediente.objects.get(id=ing_id)
                    nuevo_ingrediente = RecetaIngrediente.objects.create(
                        cantidad=float(cambios['cantidad']),
                        unidad=cambios['unidad'],
                        ingrediente=ingrediente_original.ingrediente
                    )
                    receta_modificada.receta_ingrediente.add(nuevo_ingrediente)

            # Crear Pedido
            pedido = Pedido.objects.create(
                usuario=self.usuario,
                tipo_de_orden=TipoDeOrden.objects.get(id=1),
                estado=Estado.objects.get(id=1),
                receta_pedido=receta_pedido,
                receta_modificada=receta_modificada  # Puede ser None o la nueva RecetaModificada
            )

            return pedido

        except Exception as e:
            print(f"Error al crear pedido: {str(e)}")
            return None
    
    @database_sync_to_async
    def serializar_pedido(self, pedido):
        return {
            'id': pedido.id,
            'usuario': str(pedido.usuario),
            'estado': str(pedido.estado),
            'tipo_de_orden': str(pedido.tipo_de_orden),
            'receta': str(pedido.receta_pedido.recetas.nombre_receta)
        }
