# Back-FastAPI-MongoDB

Backend construido con **FastAPI** y **MongoDB**, pensado para aplicaciones tipo e-commerce.  
Incluye manejo de usuarios, tiendas, productos, categorías, órdenes, pagos y direcciones.

## ✅ Tecnologías

- FastAPI — Framework para APIs rápidas y tipadas.  
- Uvicorn — Servidor ASGI para ejecutar FastAPI.  
- MongoDB / PyMongo — Base de datos NoSQL y su cliente oficial.  

---

## 📦 Instalación

Clona el repositorio y entra a la carpeta del proyecto:
git clone https://github.com/GabrielFuentes3g/Back-FastApi-MongoDB
cd Back-FastApi-MongoDB

Crea un entorno virtual (opcional):
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

Instala dependencias:
pip install fastapi
pip install uvicorn
pip install pymongo

(O usando requirements.txt)
pip install -r requirements.txt

---

## ▶️ Ejecutar el servidor

uvicorn main:main --reload

La API estará disponible en:
http://localhost:8000

Documentación automática:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 📁 Estructura del proyecto

/models        → Modelos Pydantic (User, Store, Product, Order…)
/schemas       → Transformación Mongo → JSON
/functions     → Lógica de negocio (CRUDs)
main.py        → Punto de entrada de la API

---

## 📚 Funcionalidades principales

### 👤 Usuarios
- Registro y login  
- Recuperación de contraseña  
- Actualización de perfil  
- Roles: customer, seller, admin  

### 🏪 Tiendas
- Crear y editar tienda  
- Actualizar logo y rating  
- Listado general y listado por usuario  

### 📦 Productos
- CRUD completo  
- Actualizar stock y precio  
- Búsqueda por nombre, descripción o categoría  

### 🧾 Órdenes
- Crear órdenes con items  
- Consultar historial por usuario  
- Actualizar estatus (pendiente, enviado, entregado)  

### 💳 Pagos
- Registrar pago  
- Actualizar método y estado  

### 📍 Direcciones
- Crear, editar y eliminar direcciones de envío  

---

## 📝 Notas

- La conexión a MongoDB usa la variable de entorno **MONGO_URI**.  
- Compatible con frontends en Next.js, React, Flutter, etc.

---
