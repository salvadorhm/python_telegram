# Python Telegram

Demos del uso de la libreria python-telegram-bot

## 1. Requisitos

Si se desea ejecutar la aplicacion en un entorno de desarrollo, se recomienda utilizar un entorno virtual. Para crear un entorno virtual, se puede utilizar el siguiente comando:

```bash
python3 -m venv .venv
```

Para activar el entorno virtual, se puede utilizar el siguiente comando:

```bash
source .venv/bin/activate
```

En el caso de Windows, el comando para activar el entorno virtual es:

```bash
.venv\Scripts\Activate.ps1
```

o

```bash
.venv\Scripts\activate.bat
```

Nota: es problable que se necesite ejecutar el siguiente comando para permitir la ejecucion de scripts en PowerShell:

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
o

```bash
Set-ExecutionPolicy Unrestricted -Scope Process
```

Para instalar las dependencias necesarias, se puede utilizar el siguiente comando:

```bash
pip install -r requirements.txt
```

## 2. Ejecución de los bots

````bash
python3 bot.py
````

## 3. Lista de demos

|No.|Carpeta|Descripción|
|--|--|--|
|01|01_echo|Ejemplo base con start, help y echo; responde con el texto que recibe.|
|02|02_audio|Ejemplo de como recibir un archivo de audio en mp3 o m4a y almacenarlo en una carpeta|
|03|03_video|Ejemplo de como recibir un archivo de video en mp4 y almacenarlo en una carpeta|
|04|04_image|Ejemplo de como recibir una imagen y almacenarlo en una carpeta|
|05|05_voice|Ejemplo de como recibir un mensaje de voz y almacenarlo en una carpeta|
|06|06_document|Ejemplo de como recibir un archivo PDF, DOCX, etc. y almacenarlo en una carpeta|
|07|07_location|Ejemplo de como recibir una ubicación (longitud, latitud) y alamcernarla en un archivo de texto.|
|08|08_sedfile|Ejemplo de como enviar un archivo a un usuario|
|09|09_sendlocation|senlocation|Ejemplo de como enviar una ubicación a un usuario|
