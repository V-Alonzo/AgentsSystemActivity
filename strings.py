TRANSLATIONS = {
    "es" : {
        "WebSearchElement" : {
            "reason" : "Por qué esta búsqueda es relevante para la consulta.",
            "query" : "El término a buscar en la web."
        },
        "WebSearchPlan" : {
            "searches" : "Lista de búsquedas a realizar."
        },
        "InformationData" : {
            "brief_summary" : "Resumen breve de la información recopilada.",
            "markdown_report" : "Informe en formato Markdown.",
            "tracking_points" : "Temas sugeridos para investigar más."
        },
        "SearchAgent":{
            "instructions" : (
                "Eres un asistente de investigación. Dado un término de bbúsqueda, buscas en la web ese término y"
                "produces un resumen conciso de los resultados. El resumen debe tener 2-3 parrafos y menos de 300"
                "palabras. Captura los puntos principales. Escribe de manera concisa, no es necesario tener oraciones"
                "completas o buena gramática. Esto será consumido por alguien que sintetiza un informe, por lo que es"
                "vital que captures la esencia e ignores cualquier relleno. No incluyas ningún comentario adicional"
                "que no sea el resumen en si"
            ),
            "name" : "AgenteBusquedaWeb"
        },
        "PlannerAgent" : {
            "instructions" : (
                "Eres un asistente de investigación útil. Dada una consulta, propón un conjunto de búsquedas web"
                "para realizar para responder mejor la consulta. Proporciona {SEARCHES_NUMBER} términos para buscar"
            ),
            "name" : "AgentePlanificadorBusquedaWeb"
        },
        "WriterAgent" : {
            "instructions" : (
                "Eres un investigador senior encargado de escribir un informe cohesivo para una consulta de investigación."
                "Se te proporcionará la consulta original y alguna investigación inicial realizada por un asistente."
                "Primero propón un esquema para el informe que describa su estructura y flujo. Luego genera el informe"
                "y devuélvelo como tu salida final. La salida final debe estar en formato markdown, y debe ser extensa"
                "y detallada. Apunta a 5-10 páginas de contenido, al menos 1000 palabras"
            ),
            "name" : "AgenteRedactor"
        },
        "Query" : "Consulta",
        "Reason" : "Razón",
        "OriginalQuery" : "Consulta original",
        "Errors" : {
            "ReadingFile" : "Error al leer el archivo",
            "InvalidReceipientEmail" : "Correo electrónico de destinatario no válido",
            "MissingEmailCredentials" : "Faltan credenciales de correo electrónico en las variables de entorno",
            "MissingRecipients" : "No se encontraron destinatarios para enviar el correo",
            "smtp_failure" : "Error al conectar con el servidor SMTP: {error}",
            "general_failure" : "Error al enviar los correos: {error}"
        },
        "Investigation" : {
            "empty_query" : "Please enter a topic to investigate.",
            "planning_searches" : "Planning searches...",
            "trace_completed" : "Investigation completed",
            "planned_searches" : "Planned {count} searches based on the query.",
            "planned_search_item" : " -> {query}",
            "performing_searches" : "Performing searches...",
            "completed_searches" : " Completed all searches: {count} results obtained.",
            "writing_report" : "\n **Writing detailed report...**",
            "report_completed" : " Report writing completed.",
            "sending_emails" : "\n **Sending emails to recipients...**",
            "sending_status" : "Sending...",
            "email_skipped" : "Email sending skipped by user."
        },
        "RecipientPreview" : {
            "upload_prompt" : "Upload your .xlsx or .csv file to preview the recipients.",
            "no_valid_recipients" : "No valid recipients found in the file. Please check the format and try again.",
            "unnamed_recipient" : "Sin nombre",
            "row_with_name" : " {name} - {email}",
            "row_without_name" : " Sin nombre - {email}",
            "valid_recipients_found" : "**{count} valid recipients found:**"
        },
        "EmailReport" : {
            "template" : '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #1a1a2e; background: #f4f6fb; margin: 0; padding: 0; }}
        .container {{ max-width: 720px; margin: 30px auto; background: #fff; border-radius: 16px;
                      box-shadow: 0 4px 24px rgba(0,0,0,0.10); overflow: hidden; }}
        .header {{ background: linear-gradient(135deg, #1a6b4a 0%, #0a3d62 100%);
                   padding: 36px 40px 24px; color: #fff; }}
        .header h1 {{ margin: 0; font-size: 22px; font-weight: 700; letter-spacing: 0.5px; }}
        .header p {{ margin: 8px 0 0; opacity: 0.85; font-size: 14px; }}
        .badge {{ display: inline-block; background: rgba(255,255,255,0.20); border-radius: 20px;
                  padding: 4px 14px; font-size: 12px; margin-top: 12px; }}
        .summary-box {{ background: #eaf4ee; border-left: 4px solid #1a6b4a; margin: 28px 40px 0;
                        padding: 16px 20px; border-radius: 8px; font-size: 15px; color: #1a6b4a; font-style: italic; }}
        .content {{ padding: 24px 40px 10px; font-size: 15px; line-height: 1.7; color: #2d2d2d; }}
        .content h1 {{ color: #0a3d62; font-size: 20px; border-bottom: 2px solid #e0e8f0; padding-bottom: 6px; }}
        .content h2 {{ color: #1a6b4a; font-size: 17px; margin-top: 24px; }}
        .content h3 {{ color: #0a3d62; font-size: 15px; }}
        .content li {{ margin-bottom: 4px; }}
        .followup {{ background: #f0f4fa; border-radius: 10px; margin: 20px 40px;
                     padding: 18px 22px; }}
        .followup h3 {{ margin: 0 0 10px; color: #0a3d62; font-size: 14px; text-transform: uppercase;
                        letter-spacing: 1px; }}
        .followup ul {{ margin: 0; padding-left: 18px; color: #444; font-size: 14px; }}
        .footer {{ text-align: center; padding: 20px; font-size: 12px; color: #aaa;
                   border-top: 1px solid #eee; }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <h1>{title}</h1>
          <p>{topic_label}: <strong>{query}</strong></p>
          <span class="badge">{badge}</span>
        </div>
        <div class="summary-box">
             {brief_summary}
        </div>
        <div class="content">
          <p>{html_body}</p>
        </div>
        <div class="followup">
          <h3>{tracking_title}</h3>
          <ul>{tracking_html}</ul>
        </div>
        <div class="footer">{footer}</div>
      </div>
    </body>
    </html>
    ''',
            "title" : "Informe de Investigación",
            "topic_label" : "Tema",
            "badge" : "Generado con IA · Sistema Multiagente",
            "tracking_title" : "Puntos para seguir investigando",
            "footer" : "Generado automáticamente por el Sistema de Investigación Multiagente"
        },
        "GradioUI" : {
            "css" : '''
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

body, .gradio-container, .main {
    background: #f0f4f8 !important;
    font-family: 'Inter', sans-serif !important;
    color: #1a202c !important;
}

#titulo {
    text-align: center;
    padding: 32px 24px 28px;
    background: linear-gradient(135deg, #1a6b4a 0%, #0a3d62 100%);
    border-radius: 14px;
    margin-bottom: 20px;
    box-shadow: 0 4px 18px rgba(10,61,98,0.18);
}
#titulo h1 {
    font-family: 'Inter', sans-serif !important;
    font-size: 1.9rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    margin: 0 0 6px !important;
    letter-spacing: -0.3px;
}
#titulo p {
    color: rgba(255,255,255,0.80);
    font-size: 0.9rem;
    margin: 0;
    font-weight: 400;
}

.block, .gr-box {
    background: #ffffff !important;
    border: 1px solid #d1dce8 !important;
    border-radius: 12px !important;
    box-shadow: 0 1px 6px rgba(0,0,0,0.06) !important;
}

label span, .label-wrap span {
    color: #2d4a6b !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.6px !important;
}

textarea, input[type="text"], input[type="search"] {
    background: #f7fafc !important;
    border: 1px solid #c8d8e8 !important;
    color: #1a202c !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.92rem !important;
}
textarea:focus, input:focus {
    border-color: #1a6b4a !important;
    box-shadow: 0 0 0 3px rgba(26,107,74,0.12) !important;
    outline: none !important;
}

button.primary, .gr-button-primary, button[variant="primary"] {
    background: linear-gradient(135deg, #1a6b4a 0%, #0a3d62 100%) !important;
    border: none !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    border-radius: 8px !important;
    color: #ffffff !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 8px rgba(26,107,74,0.25) !important;
}
button.primary:hover, .gr-button-primary:hover {
    opacity: 0.92 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(26,107,74,0.35) !important;
}

button.secondary, .gr-button-secondary, button[variant="secondary"] {
    background: #ffffff !important;
    border: 1px solid #c8d8e8 !important;
    color: #4a6080 !important;
    font-family: 'Inter', sans-serif !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
}

.tabs { background: transparent !important; }
.tab-nav { border-bottom: 2px solid #d1dce8 !important; }
.tab-nav button {
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    color: #5a7a9a !important;
    font-size: 0.88rem !important;
    border-radius: 6px 6px 0 0 !important;
    padding: 8px 16px !important;
}
.tab-nav button.selected {
    background: #ffffff !important;
    color: #1a6b4a !important;
    font-weight: 700 !important;
    border-bottom: 2px solid #1a6b4a !important;
}

.prose, .md, .markdown-body, [class*="markdown"] {
    color: #1a202c !important;
    font-size: 0.93rem !important;
    line-height: 1.7 !important;
}

input[type="checkbox"] { accent-color: #1a6b4a !important; }
.checkbox-group label, label[for] {
    color: #2d3748 !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
}

footer { display: none !important; }
''',
            "title" : "Investigador Multiagente IA",
            "header_html" : '''
        <div id="titulo">
          <h1>🔬 Investigador Multiagente con IA</h1>
          <p>Planifica búsquedas · Redacta informes · Distribuye por correo</p>
        </div>
        ''',
            "query_label" : "Tema a investigar",
            "query_placeholder" : "Ej: Cuál es tu TEMA",
            "file_label" : "Destinatarios — archivo .xlsx o .csv",
            "recipients_preview_default" : "Sube un archivo para ver los destinatarios.",
            "send_checkbox" : "Enviar informe por correo al terminar",
            "start_button" : "🚀 Iniciar investigación",
            "clear_button" : "🗑️ Limpiar",
            "env_note_html" : '''
                <p style='margin-top:14px;font-size:0.75rem;color:#7a90a8;text-align:center;font-family:Inter,sans-serif'>
                Requiere <code>CORREO_REMITENTE</code> y <code>CONTRASENA</code> en <code>.env</code>
                </p>''',
            "status_tab" : "📡 Estado del proceso",
            "status_placeholder" : "Los pasos del proceso aparecerán aquí...",
            "report_tab" : "📄 Informe completo",
            "report_placeholder" : "El informe aparecerá aquí al finalizar.",
            "summary_tab" : "📌 Resumen ejecutivo",
            "summary_placeholder" : "El resumen ejecutivo aparecerá aquí.",
            "emails_tab" : "📧 Correos enviados",
            "emails_placeholder" : "El estado del envío aparecerá aquí.",
            "preview_no_recipients" : "⚠️ No se encontraron destinatarios válidos. Asegúrate de tener columnas '{name_column}' y '{email_column}'.",
            "preview_row_with_name" : "👤 {name} — 📧 {email}",
            "preview_row_without_name" : "👤 Sin nombre — 📧 {email}",
            "preview_found" : "**{count} destinatario(s) encontrado(s):**"
        },
        "Email":{
            "body" : "Hola {name},\n\nSe ha generado un nuevo informe de investigación que podría ser de tu interés.",
            "subject" : "Nuevo informe de investigación generado",
            "success" : "Correo enviado a {email}",
            "failure" : "Error al enviar a {email}: {error}",
            "general_failure" : "Error al enviar los correos: {error}"
        }
    }
}