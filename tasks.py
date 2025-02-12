import os
import subprocess
import json
from datetime import datetime
import sqlite3
import requests
from PIL import Image
import markdown
from fastapi import HTTPException

DATA_PATH = "/data/"

def enforce_security(path):
    """Ensure access is restricted within /data/"""
    if not path.startswith(DATA_PATH):
        raise HTTPException(status_code=403, detail="Access denied")

# A1: Run data generation script
def generate_data(email):
    subprocess.run(["python3", "datagen.py", email], check=True)

# A2: Format markdown file
def format_markdown(file_path):
    enforce_security(file_path)
    subprocess.run(["npx", "prettier@3.4.2", "--write", file_path], check=True)

# A3: Count Wednesdays in dates.txt
def count_wednesdays(input_file, output_file):
    enforce_security(input_file)
    enforce_security(output_file)

    with open(input_file, "r") as f:
        dates = f.readlines()

    count = sum(1 for date in dates if datetime.strptime(date.strip(), "%Y-%m-%d").weekday() == 2)

    with open(output_file, "w") as f:
        f.write(str(count))

# B5: Run SQL Query
def run_sql_query(db_path, output_file):
    enforce_security(db_path)
    enforce_security(output_file)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'")
    result = cursor.fetchone()[0]
    
    with open(output_file, "w") as f:
        f.write(str(result))
    
    conn.close()

# B9: Convert Markdown to HTML
def convert_md_to_html(input_file, output_file):
    enforce_security(input_file)
    enforce_security(output_file)

    with open(input_file, "r") as f:
        md_content = f.read()
    
    html_content = markdown.markdown(md_content)

    with open(output_file, "w") as f:
        f.write(html_content)

