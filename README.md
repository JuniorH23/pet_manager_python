# Pet Manager

Aplicacion de escritorio en Python para administrar mascotas (perros y gatos), con interfaz Tkinter y almacenamiento en MySQL.

## Requisitos

- Python 3
- Un servidor MySQL con una base de datos compatible con la aplicacion

Instala las dependencias:

```powershell
python -m pip install -r requirements.txt
```

Configura la conexion con estas variables de entorno (si no se indican, se usan los valores predeterminados del proyecto):

```powershell
$env:PETMANAGER_DB_HOST = "127.0.0.1"
$env:PETMANAGER_DB_PORT = "3306"
$env:PETMANAGER_DB_USER = "root"
$env:PETMANAGER_DB_PASSWORD = "tu-clave"
$env:PETMANAGER_DB_NAME = "administracionmascotasbd"
```

Inicia la aplicacion desde la carpeta del proyecto:

```powershell
python .\View\frmPet.py
```

Los archivos de base de datos locales y las credenciales de `.env` se excluyen del repositorio.
