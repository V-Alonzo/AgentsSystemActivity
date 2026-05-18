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
            "MissingRecipients" : "No se encontraron destinatarios para enviar el correo"
        },
        "Email":{
            "body" : "Hola {name},\n\nSe ha generado un nuevo informe de investigación que podría ser de tu interés.",
            "subject" : "Nuevo informe de investigación generado",
            "success" : "Correo enviado a {email}",
            "failure" : "Error al enviar a {email}: {error}",
            "smtp_failure" : "Error al conectar con el servidor SMTP: {error}",
            "general_failure" : "Error al enviar los correos: {error}"
        }
    }
}