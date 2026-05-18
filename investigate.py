import asyncio
import os
import smtplib
import pandas as pd
import gradio as gr
from email.mime.text import MIMEText
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from agents import Agent, WebSearchTool, Runner, trace
from agents.model_settings import ModelSettings
from strings import TRANSLATIONS
from settings import SEARCHES_NUMBER, WRITER_AGENT_MODEL, RECIPIENT_NAME_COLUMN, RECIPIENT_EMAIL_COLUMN, EMAIL_REGEX_PATTERN, EMAIL_SERVER, EMAIL_SERVER_PORT
import re

# Models

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
    instructions = TRANSLATIONS["es"]["PlannerAgent"]["instructions"].format(SEARCHES_NUMBER=SEARCHES_NUMBER)
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
        print(f"{TRANSLATIONS['es']['Errors']['ReadingFile']}: {e}")
        return []
    
    if RECIPIENT_EMAIL_COLUMN not in df.columns:
        return []
    
    has_name = RECIPIENT_NAME_COLUMN in df.columns
    recipients = []

    for _,row in df.iterrows():
        email = row[RECIPIENT_EMAIL_COLUMN]

        if not re.match(EMAIL_REGEX_PATTERN, email):
            print(f"{TRANSLATIONS['es']['Errors']['InvalidReceipientEmail']}: {email}")
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

    return f"""
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
          <h1>Informe de Investigación</h1>
          <p>Tema: <strong>{query}</strong></p>
          <span class="badge">Generado con IA · Sistema Multiagente</span>
        </div>
        <div class="summary-box">
             {report.brief_summary}
        </div>
        <div class="content">
          <p>{html_body}</p>
        </div>
        <div class="followup">
          <h3>Puntos para seguir investigando</h3>
          <ul>{tracking_html}</ul>
        </div>
        <div class="footer">Generado automáticamente por el Sistema de Investigación Multiagente</div>
      </div>
    </body>
    </html>
    """

def send_emails(recipients: list[tuple[str, str]], query: str, report : InformationData) -> str:
    load_dotenv()
    
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")

    if not sender or not password:
        return TRANSLATIONS["es"]["Errors"]["MissingEmailCredentials"]
    
    if not recipients:
        return TRANSLATIONS["es"]["Errors"]["MissingRecipients"]
    
    html_content = generate_html_report(report, query)
    log = []

    try:
        server = smtplib.SMTP(EMAIL_SERVER, EMAIL_SERVER_PORT)
        server.starttls()
        server.login(sender, password)

        for name, email in recipients:
            msg = MIMEText(html_content, "html")
            msg["Subject"] = TRANSLATIONS["es"]["Email"]["subject"]
            msg["From"] = sender
            msg["To"] = email

            msg.attach(MIMEText(TRANSLATIONS["es"]["Email"]["body"].format(name=name or "", query=query, report_summary=report.brief_summary), "plain"))
            msg.attach(MIMEText(html_content, "html"))

            try:
                server.sendmail(sender, email, msg.as_string())
                log.append(TRANSLATIONS["es"]["Email"]["success"].format(email=email))
            except Exception as e:
                log.append(TRANSLATIONS["es"]["Email"]["failure"].format(email=email, error=e))

        server.quit()
    except smtplib.SMTPException as e:
        return TRANSLATIONS["es"]["Errors"]["smtp_failure"].format(error=e)
    except Exception as e:
        return TRANSLATIONS["es"]["Errors"]["general_failure"].format(error=e)
    
    return "\n".join(log)

