**correr comandos en capstone/proyecto/apt2**

instalar dependencias de python para el proyecto
```bash
$ pip install -r requirements.txt
```
migrar cambios de base de datos
```bash
$ python manage.py migrate
```
comando para iniciar la app con websockets
```bash
$ python -m daphne apt.asgi:application
```
comando parainciar proyecto sin websocket
```bash
$ python manage.py runserver
```

requerimientos:  
python  
mysql
