# Sistema de Inventario para la Segunda Compañia de Bomberos de Iquique: Primer Prototipo

## Descripción
Esto es **el primer prototipo** del sistema realizado el segundo semestre del año 2023. Consiste en un proyecto Django de una sola aplicación que **permite la gestión de las existencias dentro de las unidades de la compañía**. Es posible **administrar las unidades, sus compartimentos y los insumos disponibles**.

## Descargar repositorio
Usa `git clone <url>` para clonar el proyecto

## Instalación para ejecución local (desarrollo)
Para ejecutar los siguientes comandos, **posiciónate en el directorio raíz del proyecto** usando tu terminal o CLI de preferencia


### Crear entorno virtual
Necesario para almacenar las dependencias únicamente del proyecto. Crea un entorno venv11 con el siguiente comando:
```bash
python -m venv .venv
```

### Activar entorno virtual
Antes de continuar, debemos entrar/activar el entorno virtual. Para eso, ejecuta el siguiente comando (en la raíz del proyecto):
```bash
.venv/Scripts/Activate.ps1
```
Estaremos dentro del entorno virtual si vemos `(.venv)` a la izquierda del Prompt en tu terminal. Si más adelante deseas salir del entorno virtual, cierra el terminal o usa el comando `deactivate` para salir correctamente. Ejecuta los siguientes comandos con el entorno virtual activado.


### Actualizar pip (opcional)
Actualiza el gestor de paquetes de pip del entorno virtual:
```bash
python.exe -m pip install --upgrade pip
```

### Instalar las librerías necesarias
Ejecuta el siguiente comando para instalar las dependencias del requirements.txt:
```bash
pip install -r requirements.txt
```

### Crear base de datos
Debes crear la base de datos con el nombre indicado en el `conf.json`. Necesitas generar un entorno local de desarrollo. Para eso, utiliza algún software como Laragon o XAMPP. Esto te permitirá gestionar tus bases de datos locales.

Usa algún gestor de bases de datos como phpmyadmin o MySQL Workbench para crear la base de datos.


### Crear migraciones
El proyecto ya trae un archivo inicial de migraciones creado. Ejecútalo con el siguiente comando:
```bash
python manage.py migrate
```

### Poblar base de datos (opcional)
Para que la base de datos no esté vacía, incluí el script `Insert DB.sql` con registros. Sólo trae un usuario, 2 vehículos y algunos insumos.

Ejecuta este script en tu gestor de base de datos


### Iniciar proyecto
```bash
python manage.py runserver
```