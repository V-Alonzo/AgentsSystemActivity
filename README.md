# Sistema Multiagente de Investigacion

Proyecto academico en Python para investigar un tema con agentes, sintetizar resultados en un reporte y, opcionalmente, distribuirlo por correo electronico desde una interfaz web hecha con Gradio.

## Que hace actualmente

El sistema implementa un flujo completo de investigacion asistida:

1. Recibe un tema desde la interfaz.
2. Genera un plan de busquedas web con un agente planificador.
3. Ejecuta las busquedas de forma concurrente con un agente que usa herramienta de web search.
4. Redacta un reporte estructurado en Markdown y un resumen breve.
5. Genera puntos de seguimiento para continuar la investigacion.
6. Permite cargar un archivo de destinatarios y previsualizar los correos validos.
7. Si el usuario lo activa, convierte el reporte a HTML y lo envia por SMTP.

## Funcionalidades vigentes

- Planificacion automatica de consultas de investigacion.
- Ejecucion asincrona de multiples busquedas en paralelo.
- Generacion de resumen ejecutivo.
- Generacion de informe largo en Markdown.
- Generacion de puntos sugeridos para seguimiento.
- Visualizacion del estado del proceso paso a paso en la UI.
- Previsualizacion de destinatarios antes del envio.
- Lectura de destinatarios desde archivos `.csv`, `.xls` y `.xlsx` en la capa de backend.
- Validacion basica de correos electronicos mediante expresion regular.
- Conversion del informe Markdown a una plantilla HTML para correo.
- Envio de correos usando SMTP con TLS.
- Interfaz web con Gradio para ejecutar todo el flujo sin usar una CLI propia.

## Flujo del sistema

```text
Tema -> Plan de busquedas -> Busquedas web concurrentes -> Reporte y resumen -> HTML para correo -> Envio opcional
```

## Arquitectura

El proyecto se apoya en tres agentes y una capa de orquestacion:

### 1. Agente planificador

Genera un conjunto de busquedas relevantes a partir de la consulta del usuario. El numero actual de busquedas configuradas es `3`.

### 2. Agente de busqueda

Ejecuta cada consulta usando `WebSearchTool` y devuelve un resumen breve por busqueda.

### 3. Agente redactor

Recibe la consulta original junto con los resultados recopilados y devuelve:

- `brief_summary`
- `markdown_report`
- `tracking_points`

### 4. Orquestacion

La funcion `perform_investigation()` coordina el flujo completo, actualiza el progreso que ve el usuario y dispara el envio de correos cuando corresponde.

## Interfaz disponible

La aplicacion expone una interfaz Gradio con:

- Campo para ingresar el tema a investigar.
- Carga de archivo de destinatarios.
- Previsualizacion de destinatarios validos.
- Casilla para activar o desactivar el envio por correo.
- Pestañas para ver estado, informe completo, resumen ejecutivo y resultado del envio.

El punto de entrada real del proyecto está en `investigate.py` que importa y lanza la interfaz definida en `gradio_UI.py`.

## Requisitos

- Python 3.11 recomendado por `environment.yml`.
- Conexion a internet.
- Credenciales para el proveedor o modelo usado por `openai-agents`.
- Cuenta SMTP valida si se desea enviar correos.

## Dependencias actuales

El proyecto utiliza estas dependencias principales definidas en `environment.yml`:

- `gradio`
- `openai-agents`
- `pandas`
- `pydantic`
- `python-dotenv`
- `openpyxl`
- `xlrd`

## Instalacion

### Conda

```bash
conda env create -f environment.yml
conda activate AgentsSystem
```

## Variables de entorno

Se esperan las siguientes variables de entorno para el envío de correos.

```env
EMAIL_SENDER=tu_correo@example.com
EMAIL_PASSWORD=tu_app_password
```

Deben colocarse en un archivo `.env` en la raiz del proyecto.

Para ejecutar los agentes, se deben configurar las credenciales adicionales que requiere el SDK `openai-agents` en el entorno local.

## Ejecucion

Ejecuta:

```bash
python investigate.py
```

Actualmente, el script:

- crea la interfaz Gradio;
- la lanza con `share=True`;
- muestra una URL local y otra compartida cuando Gradio la habilita.

## Uso basico

1. Ejecuta la aplicacion.
2. Escribe un tema o pregunta de investigacion.
3. Opcionalmente, sube un archivo de destinatarios.
4. Activa la casilla de envio si se desea mandar el reporte por correo.
5. Inicia la investigacion.
6. Revisa las pestanas de estado, reporte, resumen y correos.

## Formato de destinatarios

La logica de lectura busca estas columnas:

- `Nombre`
- `Correo`

Ejemplo CSV:

```csv
Nombre,Correo
Ana Perez,ana@example.com
Luis Gomez,luis@example.com
```

Detalles importantes:

- Si falta la columna `Correo`, el archivo se descarta.
- La columna `Nombre` es opcional.
- El backend puede leer `.csv`, `.xls` y `.xlsx`.
- La interfaz Gradio solo permite seleccionar `.csv` y `.xlsx` desde el cargador de archivos.

## Configuracion tecnica actual

Los parametros centrales viven en `settings.py`:

- `SEARCHES_NUMBER = 3`
- `WRITER_AGENT_MODEL = "gpt-4o-mini"`
- `RECIPIENT_NAME_COLUMN = "Nombre"`
- `RECIPIENT_EMAIL_COLUMN = "Correo"`
- `EMAIL_SERVER = "smtp.gmail.com"`
- `EMAIL_SERVER_PORT = 587`

## Estructura del proyecto

```text
AgentsSystem/
├── investigate.py
├── gradio_UI.py
├── settings.py
├── strings.py
├── environment.yml
├── example.env
├── destinatarios.csv
└── README.md
```

### Archivos principales

- `investigate.py`: modelos, agentes, orquestacion, lectura de destinatarios, generacion HTML y envio SMTP.
- `gradio_UI.py`: construccion de la interfaz y enlaces entre componentes de UI y backend.
- `settings.py`: configuracion operativa del sistema.
- `strings.py`: textos de UI, agentes, logs y plantilla HTML del correo.
- `environment.yml`: entorno recomendado del proyecto.
- `destinatarios.csv`: ejemplo simple de destinatarios.

## Salidas del sistema

Cuando la ejecucion finaliza, la interfaz puede mostrar:

- bitacora del proceso;
- informe completo en Markdown;
- resumen ejecutivo;
- estado del envio de correos.