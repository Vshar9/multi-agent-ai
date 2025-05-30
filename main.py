import os
import sys
import json
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from redis_memory import RedisMemory
from utils.file_utils import extract_file_content
from agents.classifier_agent import ClassifierAgent
from agents.json_agent import JsonAgent
from agents.email_agent import EmailAgent
from agents.pdf_agent import PdfAgent

from rich.console import Console
from rich.syntax import Syntax

console = Console()


def pretty_print(title: str, data: dict):
    console.rule(f"[bold cyan]{title}")
    syntax = Syntax(
        json.dumps(data, indent=4, ensure_ascii=False),
        "json",
        theme="monokai",
        line_numbers=False
    )
    console.print(syntax)
    console.rule()


def main(filepath: str):
    console.print(f"[bold green]{datetime.now().isoformat()}[/bold green] - Processing file: [yellow]{filepath}[/yellow]")

    redis_client = RedisMemory()
    classifier = ClassifierAgent(redis_client)
    json_agent = JsonAgent(redis_client)
    email_agent = EmailAgent(redis_client)
    pdf_agent = PdfAgent(redis_client)

    file_format, content = extract_file_content(filepath)
    pretty_print("Detected Format and Raw Content", {"format": file_format, "sample": str(content)[:300]})

    text_for_intent = (
        content if isinstance(content, str) else
        content.get("body") or json.dumps(content)
    )
    intent = classifier.classify_intent(text_for_intent)
    pretty_print("Classifier Result", {"intent": intent})

    if file_format == "JSON":
        result = json_agent.validate_and_reformat(content)
        pretty_print("JSON Agent Output", result)

    elif file_format == "Email":
        result = email_agent.analyze_email(content, intent)
        pretty_print("Email Agent Output", result)

    elif file_format == "PDF":
        result = pdf_agent.analyze_pdf(content, intent)
        pretty_print("PDF Agent Output", result)

    else:
        console.print("[red]Unsupported file format. Exiting.[/red]")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        console.print("[red]Usage: python main.py <file_path>[/red]")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.isfile(input_file):
        console.print(f"[red]Error: File not found: {input_file}[/red]")
        sys.exit(1)

    main(input_file)
