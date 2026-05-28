# INTERFAZ GRADIO
import gradio as gr
from investigate import perform_investigation, read_recipient
from settings import RECIPIENT_NAME_COLUMN, RECIPIENT_EMAIL_COLUMN
from strings import TRANSLATIONS

UI_TEXT = TRANSLATIONS["es"]["GradioUI"]
CSS = UI_TEXT["css"]

def previsualizar_destinatarios(ruta):
    if not ruta:
        return UI_TEXT["recipients_preview_default"]
    destinatarios = read_recipient(ruta)
    if not destinatarios:
        return UI_TEXT["preview_no_recipients"].format(
            name_column=RECIPIENT_NAME_COLUMN,
            email_column=RECIPIENT_EMAIL_COLUMN,
        )
    filas = [
        UI_TEXT["preview_row_with_name"].format(name=nombre, email=correo)
        if nombre else UI_TEXT["preview_row_without_name"].format(email=correo)
        for nombre, correo in destinatarios
    ]
    return UI_TEXT["preview_found"].format(count=len(destinatarios)) + "\n\n" + "\n\n".join(filas)

def crear_interfaz():
    with gr.Blocks(css=CSS, title=UI_TEXT["title"]) as demo:

        gr.HTML(UI_TEXT["header_html"])

        ruta_state = gr.State(None)

        with gr.Row(equal_height=False):

            with gr.Column(scale=1, min_width=300):

                with gr.Group():
                    consulta_input = gr.Textbox(
                        label=UI_TEXT["query_label"],
                        placeholder=UI_TEXT["query_placeholder"],
                        lines=3,
                    )

                with gr.Group():
                    archivo_excel = gr.File(
                        label=UI_TEXT["file_label"],
                        file_types=[".xlsx", ".csv"],
                    )
                    destinatarios_preview = gr.Markdown(
                        value=UI_TEXT["recipients_preview_default"],
                    )

                enviar_check = gr.Checkbox(
                    label=UI_TEXT["send_checkbox"],
                    value=False,
                )

                with gr.Row():
                    btn_investigar = gr.Button(UI_TEXT["start_button"], variant="primary", scale=2)
                    btn_limpiar   = gr.Button(UI_TEXT["clear_button"], variant="secondary", scale=1)

                gr.HTML(UI_TEXT["env_note_html"])

            with gr.Column(scale=2):
                with gr.Tabs():
                    with gr.Tab(UI_TEXT["status_tab"]):
                        log_output = gr.Markdown(value=UI_TEXT["status_placeholder"])
                    with gr.Tab(UI_TEXT["report_tab"]):
                        informe_output = gr.Markdown(value=UI_TEXT["report_placeholder"])
                    with gr.Tab(UI_TEXT["summary_tab"]):
                        resumen_output = gr.Markdown(value=UI_TEXT["summary_placeholder"])
                    with gr.Tab(UI_TEXT["emails_tab"]):
                        correos_output = gr.Markdown(value=UI_TEXT["emails_placeholder"])

        # ── Eventos ──
        def al_subir_archivo(archivo):
            if archivo is None:
                return UI_TEXT["recipients_preview_default"], None
            ruta = archivo.name if hasattr(archivo, "name") else archivo
            preview = previsualizar_destinatarios(ruta)
            return preview, ruta

        archivo_excel.change(
            fn=al_subir_archivo,
            inputs=archivo_excel,
            outputs=[destinatarios_preview, ruta_state],
        )

        btn_investigar.click(
            fn=perform_investigation,
            inputs=[consulta_input, ruta_state, enviar_check],
            outputs=[log_output, informe_output, resumen_output, correos_output],
        )

        def limpiar():
            return (
                "",
                None,
                UI_TEXT["recipients_preview_default"],
                False,
                UI_TEXT["status_placeholder"],
                UI_TEXT["report_placeholder"],
                UI_TEXT["summary_placeholder"],
                UI_TEXT["emails_placeholder"],
            )

        btn_limpiar.click(
            fn=limpiar,
            outputs=[
                consulta_input, ruta_state, destinatarios_preview, enviar_check,
                log_output, informe_output, resumen_output, correos_output,
            ],
        )

    return demo