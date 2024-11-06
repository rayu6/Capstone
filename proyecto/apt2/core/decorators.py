from functools import wraps
from django.http import HttpResponseForbidden,HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from . import views
import time
def role_required(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.session.get('role') in allowed_roles:
                return view_func(request, *args, **kwargs)
            elif request.session.get('role') is None:
                messages.error(request, "Debes iniciar sesión para acceder a esta página ")
                return HttpResponseRedirect(reverse('login'))
            elif request.session.get('role') not in allowed_roles:
                messages.error(request, "No tienes permiso para acceder a esta página.")
                return HttpResponseRedirect(reverse('home'))
            
        return _wrapped_view
    return decorator