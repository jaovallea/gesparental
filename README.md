<h1 align="center">📊 GesParental</h1>
<p align="center">
  <b>Gestión Parental de Faltas y Méritos</b><br>
  Control visual y sencillo para el seguimiento de conducta y recompensas familiares 🏡
</p>

---

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-Framework-success?logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Render-AutoDeploy-46C2CB?logo=render&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" />
</p>

---

## 🧠 Descripción

**GesParental** es una app web desarrollada en **FastAPI** que permite registrar y visualizar el comportamiento de tus hijos mediante un sistema de **faltas**, **méritos** y **amonestaciones automáticas**.

Pensada para padres que quieren mantener un seguimiento claro y equilibrado entre disciplina y recompensas.

---

## 🚀 Características

✨ **Registro de faltas y méritos**  
🧮 **Gráficos circulares interactivos** (Chart.js)  
🎯 **Amonestación automática** al alcanzar 7 faltas  
🕒 **Restablecimiento automático** tras 3 días o al volver a cero  
🎨 **Interfaz visual diferenciada** (Johlexa 💜 y Alejandra 🌸)  
📱 **Compatible con dispositivos móviles**  

---

## 🧰 Tecnologías principales

| Tecnología | Uso |
|-------------|-----|
| 🐍 **Python 3.12** | Lenguaje principal |
| ⚡ **FastAPI** | Framework backend |
| 🎨 **TailwindCSS** | Estilo visual |
| 📊 **Chart.js** | Gráficos dinámicos |
| 💾 **SQLite** | Base de datos |
| 🚀 **Uvicorn** | Servidor ASGI |
| 🌍 **Render** | Despliegue automático |

---

## ⚙️ Instalación local

```bash
# 1️⃣ Clonar el repositorio
git clone https://github.com/jaovallea/gesparental.git
cd gesparental

# 2️⃣ Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3️⃣ Instalar dependencias
pip install -r requirements.txt

# 4️⃣ Ejecutar el servidor
uvicorn app.main:app --reload

Abre en tu navegador: 👉 http://127.0.0.1:8000
🌍 Despliegue en Render

La app está lista para auto-deploy gracias al archivo render.yaml.

    Conecta tu cuenta de Render.com

con GitHub.

Elige “New +” → “Blueprint” y selecciona este repositorio.

Render instalará las dependencias y desplegará automáticamente tu app.

Obtendrás una URL pública como:

    https://gesparental.onrender.com

Cada nuevo git push actualiza automáticamente la app 🎯
📁 Estructura del proyecto

gesparental/
│
├── app/
│   ├── main.py           # Lógica principal (FastAPI)
│   ├── database.py       # Configuración SQLite
│   ├── templates/        # HTML (Jinja2)
│   └── static/           # CSS, JS y gráficos
│
├── requirements.txt      # Dependencias
├── render.yaml           # Configuración Render
├── .gitignore            # Archivos ignorados
├── .gitattributes        # Normalización de texto
└── README.md             # Documentación

👨‍💻 Autor

Desarrollado por: Jaovallea


📧 Ingeniero de Sistemas – Proyecto personal de gestión familiar
🕓 Versión: 1.0.0
📄 Licencia: MIT
🌟 Vista previa (captura sugerida)

    📸 (Aquí puedes subir una captura del dashboard principal para mostrar los gráficos y colores personalizados.)

Ejemplo:

<img src="docs/preview.png" width="700" alt="GesParental Dashboard Preview">

💡 Próximas mejoras

    ✅ Exportar historial a PDF

    ✅ Sistema de notificaciones

    ✅ Panel móvil simplificado

    ✅ Modo “tareas positivas” configurable

<p align="center">✨ Hecho con ❤️ para ayudar a padres a mantener el equilibrio entre disciplina y amor ✨</p> ```