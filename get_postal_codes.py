from flask import Flask, request, render_template, send_file
import requests
import os
import threading

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        departements = request.form.get('departements').split(',')
        filename = 'codes_postaux.txt'

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

            # Create the file in the project's root directory
            with open(filename, 'w') as f:
                for code in all_codes:
                    f.write(code + "\n")

            print(f"Postal codes have been written to {filename}")
            print("Voila bg!")

        # Run the fetch_data function in a new thread
        threading.Thread(target=fetch_data).start()

        return render_template('index.html', message="Data fetching has started.")

    return render_template('index.html')

@app.route('/download', methods=['GET'])
def download():
    filename = 'codes_postaux.txt'
    if os.path.exists(filename):
        return send_file(filename, as_attachment=True)
    else:
        return "File not found", 404

if __name__ == '__main__':
    app.run()