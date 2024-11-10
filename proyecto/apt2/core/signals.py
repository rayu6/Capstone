from venv import logger
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Recetas, RecetaIngrediente

@receiver(post_save, sender=Recetas)
def broadcast_receta_update(sender, instance, created, **kwargs):
    print(f"🔔 Signal received - Receta ID: {instance.id}")
    
    channel_layer = get_channel_layer()
    print(f"📡 Channel layer type: {type(channel_layer)}")
    
    data = {
        "nombre_receta": str(instance.nombre_receta.nombre),  # Acceder al nombre
        "descripcion": str(instance.descripcion),
        "link": str(instance.link),
    }
    
    try:
        print("🚀 Sending to channel layer:", {
            "type": "broadcast_db_update",
            "receta_id": instance.id,
            "data": data
        })
        
        async_to_sync(channel_layer.group_send)(
            "recetas_group",
            {
                "type": "broadcast_db_update",
                "receta_id": instance.id,
                "data": data
            }
        )
        print("✅ Message sent to channel layer successfully")
    except Exception as e:
        print(f"❌ Error in broadcast_receta_update: {str(e)}")
        import traceback
        print(traceback.format_exc())