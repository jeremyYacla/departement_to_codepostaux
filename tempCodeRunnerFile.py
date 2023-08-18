from flask import Flask, request, jsonify, send_file, render_template
import requests
import os
import threading
import uuid
from time import sleep
import sqlite3
import datetime
import logging

app = Flask(__name__)

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

POSTAL_CODES_DIR = 'postal_codes'
ALL_DEPTS = set([str(i) for i in range(1, 96)] + ['2A', '2B'])

# Assurez-vous que le dossier postal_codes existe
if not os.path.exists(POSTAL_CODES_DIR):
    os.makedirs(POSTAL_CODES_DIR)

def init_db():
    conn = sqlite3.connect('cache.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS codes_postaux (
        departement TEXT PRIMARY KEY,
        codes TEXT,
        derniere_mise_a_jour DATE
    )
    ''')
    conn.commit()
    conn.close()
    logger.info("Database initialized.")

init_db()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        departements = set(request.form.get('departements').split(','))
        missing_departements = ALL_DEPTS - departements

        if "20" in departements:
            departements.remove("20")
            departements.add("2A")
            departements.add("2B")

        logger.info(f"Received POST request with departments: {departements}")

        unique_id = uuid.uuid4()
        filename = os.path.join(POSTAL_CODES_DIR, f'codes_postaux_{unique_id}.txt')

        def fetch_data():
            try:
                all_codes = []
                today = datetime.date.today()

                for dep in departements:
                    logger.info(f"Processing department: {dep}")
                    conn = sqlite3.connect('cache.db')
                    c = conn.cursor()
                    c.execute("SELECT codes, derniere_mise_a_jour FROM codes_postaux WHERE departement=?", (dep,))
                    row = c.fetchone()

                    if row and (today - datetime.datetime.strptime(row[1], '%Y-%m-%d').date()).days < 30:
                        logger.info(f"Using cached data for department: {dep}")
                        all_codes.extend(row[0].split(','))
                    else:
                        logger.info(f"Fetching data from API for department: {dep}")
                        response = requests.get(f"https://geo.api.gouv.fr/departements/{dep}/communes")
                        data = response.json()
                        dep_codes = []
                        for commune in data:
                            if 'codesPostaux' in commune:
                                dep_codes.extend(commune['codesPostaux'])
                        all_codes.extend(dep_codes)

                        logger.info(f"Updating database for department: {dep}")
                        c.execute("REPLACE INTO codes_postaux (departement, codes, derniere_mise_a_jour) VALUES (?, ?, ?)", 
                                  (dep, ','.join(dep_codes), str(today)))
                        conn.commit()

                    conn.close()

                logger.info(f"Writing to file: {filename}")
                with open(filename, 'w') as f:
                    for code in all_codes:
                        f.write(code + "\n")

            except Exception as e:
                logger.error(f"Error in fetch_data thread: {e}")

        threading.Thread(target=fetch_data).start()

        return jsonify(message="Data fetching has started.", unique_id=str(unique_id), missing_departments=list(missing_departements))

    return render_template('index.html')

@app.route('/status/<unique_id>', methods=['GET'])
def check_status(unique_id):
    filename = os.path.join(POSTAL_CODES_DIR, f'codes_postaux_{unique_id}.txt')
    if os.path.exists(filename):
        return jsonify(status="ready")
    else:
        return jsonify(status="pending", message="Processing"), 202

@app.route('/download/<unique_id>', methods=['GET'])
def download(unique_id):
    filename = os.path.join(POSTAL_CODES_DIR, f'codes_postaux_{unique_id}.txt')
    if os.path.exists(filename):
        logger.info(f"Sending file: {filename}")
        return send_file(filename, as_attachment=True, download_name='codes_postaux.txt')
    else:
        logger.error(f"File not found: {filename}")
        return jsonify(error="File not found"), 404

if __name__ == '__main__':
    logger.info("Starting the application...")
    from waitress import serve
    serve(app, host="0.0.0.0", port=5001)
