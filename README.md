# 🤖 ChatBot WhatsApp con RAG + Google Gemini AI

Un chatbot inteligente para WhatsApp que utiliza Google Gemini AI y RAG (Retrieval-Augmented Generation) para responder preguntas basadas en documentos PDF.

## 🚀 Características

- **Integración WhatsApp**: Usa WaSenderAPI (no requiere API oficial de Meta)
- **IA Avanzada**: Powered by Google Gemini 2.0 Flash
- **RAG System**: Búsqueda semántica en documentos PDF con FAISS
- **Personalidad Configurable**: Define el tono y estilo del bot
- **División de Mensajes**: Maneja automáticamente mensajes largos
- **Historial Conversacional**: Mantiene contexto por usuario
- **Logging Completo**: Para debugging y monitoreo

## 🏗️ Arquitectura

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│    WhatsApp     │ -> │   WaSender   │ -> │  Flask Server   │
│     Usuario     │    │     API      │    │   (webhook)     │
└─────────────────┘    └──────────────┘    └─────────────────┘
                                                     │
                                                     v
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│  Google Gemini  │ <- │     RAG      │ <- │   Procesador    │
│      AI         │    │   (FAISS)    │    │   Mensajes      │
└─────────────────┘    └──────────────┘    └─────────────────┘
```

## 📋 Requisitos Previos

- Python 3.8+
- Cuenta en [Google AI Studio](https://aistudio.google.com/) (API Key gratuita)
- Cuenta en [WaSenderAPI](https://wasenderapi.com/) (para WhatsApp)
- ngrok (para exponer webhook localmente)

## 🛠️ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/mafermontoya/ChatbotWhatsapp.git
cd ChatbotWhatsapp
```

### 2. Crear entorno virtual

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# APIs obligatorias
GEMINI_API_KEY=tu_api_key_de_gemini
WASENDER_API_TOKEN=tu_token_de_wasender

# Configuraciones opcionales
GEMINI_MODEL=gemini-2.0-flash
GEMINI_EMBED_MODEL=text-embedding-004
CONVERSATIONS_DIR=conversations
RAG_INDEX_DIR=data/index
PDF_DIR=data/pdfs
WEBHOOK_SECRET=tu_secreto_webhook

# Configuraciones de mensaje
MAX_RETRIES=3
MESSAGE_CHUNK_MAX_LINES=3
MESSAGE_CHUNK_MAX_CHARS=100
MESSAGE_DELAY_MIN=0.55
MESSAGE_DELAY_MAX=1.5
```

## 📁 Estructura del Proyecto

```
ChatbotWhatsapp/
├── script.py                 # Servidor principal Flask + lógica bot
├── message_splitter.py       # Divide mensajes largos
├── persona.json             # Personalidad del bot
├── requirements.txt         # Dependencias principales
├── requirements-dev.txt     # Dependencias de desarrollo
├── .env                     # Variables de entorno (crear)
├── data/
│   ├── pdfs/               # PDFs para indexar (crear carpeta)
│   └── index/
│       ├── index_pdfs.py   # Script de indexación RAG
│       ├── index.faiss     # Índice vectorial (se genera)
│       └── docstore.json   # Metadatos chunks (se genera)
└── conversations/          # Historial por usuario (se crea automático)
```

## 🚀 Uso

### 1. Preparar documentos (Opcional)

```bash
# Crear carpeta para PDFs
mkdir data\pdfs

# Copiar tus PDFs a data/pdfs/
# Luego indexar para RAG
python data\index\index_pdfs.py
```

### 2. Ejecutar el chatbot

```bash
python script.py
```

El servidor se ejecutará en `http://localhost:5000`

### 3. Configurar webhook

```bash
# Instalar ngrok si no lo tienes
# Exponer el servidor local
ngrok http 5000

# Copiar la URL de ngrok (ej: https://abc123.ngrok.io)
# Configurar en WaSenderAPI: https://abc123.ngrok.io/webhook
```

### 4. ¡Usar el bot!

Envía un mensaje WhatsApp al número conectado en WaSenderAPI. El bot responderá automáticamente usando la información de tus PDFs.

## ⚙️ Configuración

### Personalidad del Bot

Edita `persona.json` para personalizar el comportamiento:

```json
{
  "name": "Mi Asistente",
  "description": "Descripción de la personalidad",
  "base_prompt": "Instrucciones base para el comportamiento"
}
```

### Variables de Entorno Importantes

| Variable | Descripción | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | API Key de Google Gemini | **Obligatoria** |
| `WASENDER_API_TOKEN` | Token de WaSenderAPI | **Obligatoria** |
| `GEMINI_MODEL` | Modelo de Gemini | `gemini-2.0-flash` |
| `RAG_INDEX_DIR` | Directorio del índice RAG | `data/index` |
| `PDF_DIR` | Directorio de PDFs | `data/pdfs` |

## 🧪 Testing

```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Ejecutar tests
python run_all_test.py
```

## 🔧 API Endpoints

| Endpoint | Método | Descripción |
|----------|---------|-------------|
| `/webhook` | POST | Recibe mensajes de WhatsApp |
| `/health` | GET | Health check del servidor |

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-feature`)
3. Commit tus cambios (`git commit -am 'Añadir nueva feature'`)
4. Push a la rama (`git push origin feature/nueva-feature`)
5. Crear Pull Request

## 📝 Licencia

Este proyecto está bajo la licencia MIT.

## 🆘 Soporte

- **Issues**: [GitHub Issues](https://github.com/mafermontoya/ChatbotWhatsapp/issues)
- **Documentación**: Ver este README
- **WaSenderAPI**: [Documentación oficial](https://wasenderapi.com/docs)
- **Google Gemini**: [AI Studio](https://aistudio.google.com/)

## 🏷️ Versiones

- **v1.0.0**: Versión inicial con RAG + Gemini AI

---

Desarrollado con ❤️ usando Google Gemini AI y FAISS
