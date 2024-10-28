from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Recetas, RecetaIngrediente

@receiver(post_save, sender=Recetas)
def broadcast_receta_update(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    
    # Preparar datos para enviar
    data = {
        'nombre_receta': str(instance.nombre_receta),
        'descripcion': instance.descripcion,
        'link': instance.link,
    }
    
    # Enviar actualización a todos los clientes conectados
    async_to_sync(channel_layer.group_send)(
        "recetas_group",
        {
            "type": "broadcast_db_update",
            "receta_id": instance.id,
            "data": data
        }
    )

@receiver(post_save, sender=RecetaIngrediente)
def broadcast_ingrediente_update(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    
    # Preparar datos para enviar
    data = {
        'ingrediente': str(instance.ingrediente),
        'cantidad': str(instance.cantidad),
        'unidad': instance.unidad
    }
    
    # Enviar actualización a todos los clientes conectados
    async_to_sync(channel_layer.group_send)(
        "recetas_group",
        {
            "type": "broadcast_db_update",
            "receta_id": instance.id,
            "data": data
        }
    )