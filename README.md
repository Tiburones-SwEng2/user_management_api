# API REST - Gestion y acceso de usuarios

API creada para la gestion de usuarios y acceso de usuarios dentro del sistema Donatello

## Ejecucion de la API

Para ejecutar la API primero hay que crear un entorno virtual y activarlo con los siguientes comandos:

```bash
python -m venv venv
.\venv\Scripts\activate
```

Una vez dentro del entorno virtual, se deben instalar las librerias usados con el siguiente comando:

```bash
pip install -r requirements.txt
```

Por ultimo se ejecuta la API con el siguiente comando:

```bash
python app.py
```

Esto hara que la API se ejecuta en la URL http://127.0.0.1:5002 y su documentacion en Swagger se encontrara en http://127.0.0.1:5002/apidocs

## Endpoints disponibles

### POST /register

Encargado de registrar al usuario dentro del sistema

#### Ejemplo

URL: http://127.0.0.1:5002/register

Body:

```json
{
  "name": "Juan",
  "email": "example@example.com",
  "password": "1234"
}
```

Respuesta:

```json
{
  "mensaje": "Usuario registrado"
}
```

### POST /login

Encargado de permitir el login del usuarios, dandole un token de acceso tipo JWT

#### Ejemplo

URL: http://127.0.0.1:5002/login

Body:

```json
{
  "email": "example@example.com",
  "password": "1234"
}
```

Respuesta:

```json
{
  "name": "Juan",
  "email": "example@example.com",
  "admin": "false",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1MjI2NjU4MSwianRpIjoiMDhlOTkxNTMtNjVlMC00ZDI2LWI2MzktNDBiY2ExZmMzMGZiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImV4YW1wbGVAZXhhbXBsZS5jb20iLCJuYmYiOjE3NTIyNjY1ODEsImNzcmYiOiIzN2NhZjcxOC1kY2JiLTQ3ZDEtYmMxZC1mNzAwN2RhOWJmYWEiLCJleHAiOjE3NTIyNjc0ODF9.vU3pnee8AhmhbVhOP26mA_rTDQ4EdrrV8GTw9U5UfAI"
}
```

### POST /recover

Encargado de generar un nuevo clave para el usuario en caso de que haya perdido la original.

#### Ejemplo

URL: http://127.0.0.1:5002/recover

Body:

```json
{
  "email": "nofovag693@jxbav.com"
}
```

Respuesta:

```json
{
  "mensaje": "La nueva contraseña fue entregada"
}
```
