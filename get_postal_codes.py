from flask import Flask, request, jsonify, send_file, render_template
import requests
import os
import threading
import uuid

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        departements = request.form.get('departements').split(',')

        unique_id = uuid.uuid4()
        filename = f'codes_postaux_{unique_id}.txt'

        def fetch_data():
            all_codes = []
            for dep in departements:
                print(f"Fetching data for department: {dep}")
                response = requests.get(f"https://geo.api.gouv.fr/departements/{dep}/communes")
                data = response.json()
                for commune in data:
                    if 'codesPostaux' in commune:
                        all_codes.extend(commune['codesPostaux'])
                    else:
                        print(f"No postal codes found for commune: {commune['nom']}")

            print(f"Total postal codes found: {len(all_codes)}")

            # Create the file with the unique filename
            with open(filename, 'w') as f:
                for code in all_codes:
                    f.write(code + "\n")

            print(f"Postal codes have been written to {filename}")
            print("Voila bg!")

        # Run the fetch_data function in a new thread
        threading.Thread(target=fetch_data).start()

        return jsonify(message="Data fetching has started.", unique_id=str(unique_id))

    return render_template('index.html')

@app.route('/download/<unique_id>', methods=['GET'])
def download(unique_id):
    filename = f'codes_postaux_{unique_id}.txt'
    if os.path.exists(filename):
        return send_file(filename, as_attachment=True, download_name='codes_postaux.txt')
    else:
        return "File not found", 404

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=80)
