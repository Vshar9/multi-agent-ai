import os
import json
import pdfplumber
import re
from email.utils import parseaddr
from email import message_from_string
from typing import Tuple,Optional,Any

def detect_format(file_path :str) -> Optional[str]:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return "PDF"
    elif ext == ".json":
        return "JSON"
    elif ext in [".txt",".eml"]:
        return "Email"
    else :
        return None

def read_pdf(file_path: str)->str:
    with pdfplumber.open(file_path) as pdf:
        return '\n'.join(page.extract_text() or "" for page in pdf.pages)

def read_json(file_path: str)->dict:
    with open(file_path, 'r',encoding='utf-8') as f:
        return json.load(f)
    
def read_email(file_path:str)->dict:
    with open(file_path,'r',encoding='utf-8') as f:
        raw_email = f.read()
    
    msg = message_from_string(raw_email)
    sender = parseaddr(msg.get('from',''))
    subject = msg.get('Subject','')
    body = msg.get_payload(decode=False)

    return{
        "sender": sender,
        "subject": subject,
        "body": body
    }

def extract_file_content(file_path: str)->Tuple[str,any]:
    fmt = detect_format(file_path)
    if not fmt: 
        raise ValueError(f"Unsupported file format: {file_path}")

    if fmt == 'PDF':
        retVal = read_pdf(file_path)
    elif fmt == 'JSON':
        retVal = read_json(file_path)
    elif fmt == 'Email':
        retVal = read_email(file_path)
    else:
        raise ValueError(f"Unreachable code")

    return fmt,retVal

if __name__ == "__main__":
    path = "./sample_files/sample.json"
    fmt, content = extract_file_content(path)
    print("Detected Format:", fmt)
    print("Content Snippet:", str(content))
