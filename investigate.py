import asyncio
import os
import smtplib
import pandas as pd
import gradio as gr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from agents import Agent, WebSearchTool, Runner, trace
from agents.model_settings import ModelSettings
from strings import TRANSLATIONS
from settings import SEARCHES_NUMBER, WRITER_AGENT_MODEL, RECIPIENT_NAME_COLUMN, RECIPIENT_EMAIL_COLUMN, EMAIL_REGEX_PATTERN, EMAIL_SERVER, EMAIL_SERVER_PORT
import re

# Models

load_dotenv()
TEXT = TRANSLATIONS["es"]
INVESTIGATION_TEXT = TEXT["Investigation"]
RECIPIENT_PREVIEW_TEXT = TEXT["RecipientPreview"]
EMAIL_REPORT_TEXT = TEXT["EmailReport"]
ERROR_TEXT = TEXT["Errors"]
EMAIL_TEXT = TEXT["Email"]

class WebSearchElement(BaseModel):
    reason: str = Field(description=TRANSLATIONS["es"]["WebSearchElement"]["reason"])
    query: str = Field(description=TRANSLATIONS["es"]["WebSearchElement"]["query"])
    
class WebSearchPlan(BaseModel):
    searches: list[WebSearchElement] = Field(description = TRANSLATIONS["es"]["WebSearchPlan"]["searches"])

class InformationData(BaseModel):
    brief_summary: str = Field(description=TRANSLATIONS["es"]["InformationData"]["brief_summary"])
    markdown_report : str = Field(description=TRANSLATIONS["es"]["InformationData"]["markdown_report"])
    tracking_points : list[str] = Field(description=TRANSLATIONS["es"]["InformationData"]["tracking_points"])


search_agent = Agent(
    name=TRANSLATIONS["es"]["SearchAgent"]["name"],
    instructions = TRANSLATIONS["es"]["SearchAgent"]["instructions"],
    tools = [WebSearchTool(search_context_size="low")],
    model = "gpt-4o-mini",
    model_settings = ModelSettings(tool_choice = "required")
)

planner_agent = Agent(
    name = TRANSLATIONS["es"]["PlannerAgent"]["name"],
    instructions = TRANSLATIONS["es"]["PlannerAgent"]["instructions"].format(SEARCHES_NUMBER=SEARCHES_NUMBER),
    output_type=WebSearchPlan
)

writer_agent = Agent(
    name=TRANSLATIONS["es"]["WriterAgent"]["name"],
    instructions=TRANSLATIONS["es"]["WriterAgent"]["instructions"],
    model=WRITER_AGENT_MODEL,
    output_type=InformationData
)

async def search(element: WebSearchElement) -> str:
    search_input = f"{TRANSLATIONS['es']['Query']}: {element.query}\n{TRANSLATIONS['es']['Reason']}: {element.reason}"
    result = await Runner.run(search_agent, search_input)
    return result.final_output

async def plan_searches(query: str) -> WebSearchPlan:
    result = await Runner.run(planner_agent, f"{TRANSLATIONS['es']['Query']}: {query}")
    return result.final_output

async def perform_searches(plan: WebSearchPlan) -> list[str]:
    tasks = [asyncio.create_task(search(elem)) for elem in plan.searches]
    return await asyncio.gather(*tasks)

async def write_report(query: str, results: list[str]) -> InformationData:
    research_input = f"{TRANSLATIONS['es']['OriginalQuery']}: {query}\n{TRANSLATIONS['es']['InformationData']['brief_summary']}:\n" + "\n\n".join(results)
    result = await Runner.run(writer_agent, research_input)
    return result.final_output

async def perform_investigation(
        query: str,
        excel_filepath: str,
        send: bool,
        progress: gr.Progress = gr.Progress(track_tqdm=True)
):
    """
    Main function that orchestates the whole pipeline and update de Gradio's UI.
    Yield: (status_log, report_markdown, short_summary, email_log)
    """

    if not query.strip():
        yield INVESTIGATION_TEXT["empty_query"], "", "", ""
        return
    
    log = []

    # Step 1: Plan searches
    log.append(INVESTIGATION_TEXT["planning_searches"])

    yield "\n".join(log), "", "", ""

    with trace(INVESTIGATION_TEXT["trace_completed"]):
        plan = await plan_searches(query)

    concepts = [elem.query for elem in plan.searches]
    log.append(INVESTIGATION_TEXT["planned_searches"].format(count=len(concepts)))

    for t in concepts:
        log.append(INVESTIGATION_TEXT["planned_search_item"].format(query=t))

    yield "\n".join(log), "", "", ""

    # Step 2: Perform parallel searches
    log.append(INVESTIGATION_TEXT["performing_searches"])
    yield "\n".join(log), "", "", ""

    results = await perform_searches(plan)
    log.append(INVESTIGATION_TEXT["completed_searches"].format(count=len(results)))

    yield "\n".join(log), "", "", ""

    # Step 3: Write report
    log.append(INVESTIGATION_TEXT["writing_report"])
    yield "\n".join(log), "", "", ""

    report = await write_report(query, results)
    log.append(INVESTIGATION_TEXT["report_completed"])
    yield "\n".join(log), report.markdown_report, f" {report.brief_summary}", ""

    # Step 4: send emails (optional)
    status_emails = ""

    if send:
        log.append(INVESTIGATION_TEXT["sending_emails"])
        yield "\n".join(log), report.markdown_report, f" {report.brief_summary}", INVESTIGATION_TEXT["sending_status"]

        recipients = read_recipient(excel_filepath) if excel_filepath else []
        status_emails = send_emails(recipients, query, report)

        log.append(status_emails)

        yield "\n".join(log), report.markdown_report, f" {report.brief_summary}", status_emails
    
    else:
        yield "\n".join(log), report.markdown_report, f" {report.brief_summary}", INVESTIGATION_TEXT["email_skipped"]


def get_path(file) -> str:
    if file is None:
        return None
    
    return file.name if hasattr(file, "name") else file


# Load recipients
def preview_recipients(file) -> str:
    if not file:
        return RECIPIENT_PREVIEW_TEXT["upload_prompt"]
    
    route = file.name if hasattr(file, "name") else file
    receipients = read_recipient(route)

    if not receipients:
        return RECIPIENT_PREVIEW_TEXT["no_valid_recipients"]
    
    rows = [
        RECIPIENT_PREVIEW_TEXT["row_with_name"].format(name=name, email=email)
        if name else RECIPIENT_PREVIEW_TEXT["row_without_name"].format(email=email)
        for name, email in receipients
    ]
    return RECIPIENT_PREVIEW_TEXT["valid_recipients_found"].format(count=len(receipients)) + "\n\n" + "\n\n".join(rows)

def read_recipient(filepath : str) -> list[tuple[str, str]]:
    if not filepath or not os.path.exists(filepath):
        return []
    
    ext = os.path.splitext(filepath)[1].lower()

    try:
        if ext == ".csv":
            df = pd.read_csv(filepath)
        elif ext in [".xls", ".xlsx"]:
            df = pd.read_excel(filepath)
    except Exception as e:
        print(f"{ERROR_TEXT['ReadingFile']}: {e}")
        return []
    
    if RECIPIENT_EMAIL_COLUMN not in df.columns:
        return []
    
    has_name = RECIPIENT_NAME_COLUMN in df.columns
    recipients = []

    for _,row in df.iterrows():
        email = row[RECIPIENT_EMAIL_COLUMN]

        if not re.match(EMAIL_REGEX_PATTERN, email):
            print(f"{ERROR_TEXT['InvalidReceipientEmail']}: {email}")
            continue

        name = row[RECIPIENT_NAME_COLUMN] if has_name else ""
        recipients.append((name, email))

    return recipients

def generate_html_report(report : InformationData, query: str) -> str:
    md = report.markdown_report

    html_body = md

    html_body = md
    html_body = re.sub(r"^### (.+)$", r"<h3>\1</h3>", html_body, flags=re.MULTILINE)
    html_body = re.sub(r"^## (.+)$", r"<h2>\1</h2>", html_body, flags=re.MULTILINE)
    html_body = re.sub(r"^# (.+)$", r"<h1>\1</h1>", html_body, flags=re.MULTILINE)
    html_body = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html_body)
    html_body = re.sub(r"\*(.+?)\*", r"<em>\1</em>", html_body)
    html_body = re.sub(r"^- (.+)$", r"<li>\1</li>", html_body, flags=re.MULTILINE)
    html_body = html_body.replace("\n\n", "</p><p>")

    tracking_html = "".join(f"<li>{p}</li>" for p in report.tracking_points)

    return EMAIL_REPORT_TEXT["template"].format(
        title=EMAIL_REPORT_TEXT["title"],
        topic_label=EMAIL_REPORT_TEXT["topic_label"],
        query=query,
        badge=EMAIL_REPORT_TEXT["badge"],
        brief_summary=report.brief_summary,
        html_body=html_body,
        tracking_title=EMAIL_REPORT_TEXT["tracking_title"],
        tracking_html=tracking_html,
        footer=EMAIL_REPORT_TEXT["footer"],
    )

def send_emails(recipients: list[tuple[str, str]], query: str, report : InformationData) -> str:
    load_dotenv()
    
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")

    if not sender or not password:
        return ERROR_TEXT["MissingEmailCredentials"]
    
    if not recipients:
        return ERROR_TEXT["MissingRecipients"]
    
    html_content = generate_html_report(report, query)
    log = []

    try:
        server = smtplib.SMTP(EMAIL_SERVER, EMAIL_SERVER_PORT)
        server.starttls()
        server.login(sender, password)

        for name, email in recipients:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = EMAIL_TEXT["subject"]
            msg["From"] = sender
            msg["To"] = email

            plain_text = EMAIL_TEXT["body"].format(
                name=name or "",
                query=query,
                report_summary=report.brief_summary,
            )

            msg.attach(MIMEText(plain_text, "plain", "utf-8"))
            msg.attach(MIMEText(html_content, "html", "utf-8"))

            try:
                server.sendmail(sender, email, msg.as_string())
                log.append(EMAIL_TEXT["success"].format(email=email))
            except Exception as e:
                log.append(EMAIL_TEXT["failure"].format(email=email, error=e))

        server.quit()
    except smtplib.SMTPException as e:
        return ERROR_TEXT["smtp_failure"].format(error=e)
    except Exception as e:
        return ERROR_TEXT["general_failure"].format(error=e)
    
    return "\n".join(log)


if __name__ == "__main__":
    from gradio_UI import crear_interfaz
    demo = crear_interfaz()
    demo.launch()