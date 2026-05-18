# Actividad de Sistema de Agentes

Proyecto académico enfocado en la construcción de un sistema multiagente para automatizar tareas de investigación web, síntesis de información y distribución de resultados por correo electrónico.

## Descripción del proyecto

Este proyecto implementa un flujo de investigación asistido por agentes en Python. A partir de una consulta, el sistema genera un plan de búsquedas, ejecuta investigaciones en la web, consolida los hallazgos en un reporte estructurado y, de forma opcional, prepara el envío del resultado por correo a una lista de destinatarios.

La lógica principal está concentrada en un único módulo que coordina agentes especializados, configuraciones de negocio, traducciones y lectura de destinatarios desde archivos tabulares.

## Objetivo del proyecto

Desarrollar una solución que demuestre cómo un enfoque multiagente puede dividir una tarea compleja de investigación en etapas especializadas para:

- planear búsquedas relevantes;
- recopilar información desde la web;
- redactar un informe coherente y detallado;
- facilitar la distribución automática del reporte a varios destinatarios.

## Funcionalidades principales

- Generación de un plan de investigación con un número configurable de búsquedas.
- Ejecución asíncrona de búsquedas web usando un agente con herramienta de búsqueda integrada.
- Síntesis de resultados en un resumen breve y un reporte completo en formato Markdown.
- Generación de puntos de seguimiento para ampliar la investigación posterior.
- Conversión del reporte a una plantilla HTML lista para enviarse por correo.
- Lectura de destinatarios desde archivos `.csv`, `.xls` o `.xlsx`.
- Validación básica de correos electrónicos antes del envío.
- Envío de reportes por SMTP usando credenciales definidas en variables de entorno.
- Centralización de mensajes y textos del sistema en español mediante un archivo de traducciones.

## Arquitectura general

El sistema está organizado alrededor de tres agentes y un conjunto de funciones de orquestación:

1. **Agente planificador**
   Recibe la consulta del usuario y propone varias búsquedas relevantes para responder mejor al tema.

2. **Agente de búsqueda**
   Ejecuta cada búsqueda en la web y devuelve resúmenes concisos de los resultados encontrados.

3. **Agente redactor**
   Toma la consulta original junto con los resultados recuperados y genera un informe final estructurado.

4. **Capa de orquestación**
   Coordina el flujo asíncrono: planificación, búsquedas concurrentes, redacción, formateo HTML y envío por correo.

5. **Capa de configuración y soporte**
   Incluye constantes de configuración, traducciones y utilidades para lectura de destinatarios.

### Flujo general

`Consulta -> Plan de búsquedas -> Búsquedas web -> Síntesis del reporte -> Conversión a HTML -> Envío por correo`

## Requisitos técnicos

### Software base

- Python 3.10 o superior.
- Acceso a internet para la investigación web.
- Cuenta de correo SMTP compatible con TLS, actualmente configurada para Gmail.

### Dependencias principales

- `pandas`
- `gradio`
- `python-dotenv`
- `pydantic`
- SDK de agentes usado por `from agents import Agent, WebSearchTool, Runner, trace`

### Variables de entorno

El archivo de ejemplo `example.env` define las credenciales mínimas para el envío de correos:

- `EMAIL_SENDER`
- `EMAIL_PASSWORD`

Además, para ejecutar los agentes y el acceso al modelo, también deben configurarse las credenciales requeridas por el SDK utilizado en el proyecto.

### Configuración relevante

En `settings.py` se definen parámetros como:

- número de búsquedas a ejecutar;
- modelo del agente redactor;
- nombres de columnas para destinatarios;
- patrón de validación de correo;
- servidor y puerto SMTP.

## Estructura relevante del proyecto

```text
AgentsSystem/
├── investigate.py      # Lógica principal del sistema multiagente
├── settings.py         # Constantes de configuración técnica y operativa
├── strings.py          # Textos e instrucciones en español para los agentes
├── destinatarios.csv   # Ejemplo de archivo con destinatarios
├── example.env         # Ejemplo de variables de entorno para correo
└── README.md           # Documentación del proyecto
```

### Descripción de archivos clave

- `investigate.py`: define los modelos de datos, los agentes, las funciones asíncronas de búsqueda y redacción, la lectura de destinatarios y el envío de correos.
- `settings.py`: concentra la configuración del flujo, el modelo y los parámetros del envío.
- `strings.py`: contiene las instrucciones de los agentes y los mensajes del sistema en español.
- `destinatarios.csv`: archivo de ejemplo para pruebas de distribución del reporte.
- `example.env`: plantilla de configuración para las credenciales de correo.

## Valor académico del proyecto

Esta actividad demuestra cómo un sistema de agentes puede distribuir responsabilidades entre planificación, recuperación de información y generación de contenido, manteniendo una separación clara entre configuración, lógica de negocio y salida final.