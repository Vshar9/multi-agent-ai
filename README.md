# Multi-Agent AI System

## Overview

This project implements a multi-agent AI system that processes inputs in various formats (PDF, JSON, Email), classifies the format and intent, and routes the data to specialized agents for processing. The system maintains shared context using Redis to enable traceability and chaining of processing steps.

---

## Features

- **Format Detection:** Supports PDF, JSON, and Email inputs.
- **Intent Classification:** Classifies intent types such as Invoice, RFQ, Complaint, etc.
- **Specialized Agents:**
  - **Classifier Agent:** Detects format and intent, routes to appropriate agent.
  - **JSON Agent:** Validates and reformats JSON data.
  - **Email Agent:** Extracts sender, subject, and body information.
  - **PDF Agent:** Summarizes content and extracts keywords.
- **Shared Memory:** Uses Redis for logging, shared state, and traceability.
- **Command-line Interface:** Run processing on input files with ease.
- **Rich CLI Output:** Uses `rich` for clean, readable results.

---

## Tech Stack

- Python 3.8+
- Redis (for shared context and logs)
- Sentence Transformers (`sentence-transformers`) for embedding-based classification
- Joblib for model serialization
- pdfplumber for PDF parsing
- Rich for enhanced CLI output formatting

---

## Installation

1. Clone the repo:

    ```bash
    git clone https://github.com/Vshar9/multi-agent-ai.git
    cd multi-agent-ai
    ```

2. Create a virtual environment and activate it (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate        # On Linux/Mac
    venv\Scripts\activate           # On Windows
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up Redis and configure your `.env` file:

    ```env
    REDIS_HOST=localhost
    REDIS_PORT=6379
    REDIS_DB=0
    REDIS_USERNAME=
    REDIS_PASSWORD=
    ```

---

## Usage

Run the main orchestrator with a file path as an argument:

```bash
python main.py <path_to_input_file>
