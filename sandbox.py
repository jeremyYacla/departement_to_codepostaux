import requests
import os

departements = ['01', '02', '03', '08', '10', '14', '21', '22', '25', '27', '35', '39', '42', '43', '44', '50', '51', '52', '53', '54', '55', '57', '59', '60', '62', '63', '67', '68', '70', '71', '74', '76', '80', '88', '89', '90']

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

# Specifying the directory where to save the file
output_dir = "<path to directory where to>"
output_file = os.path.join(output_dir, 'codes_postaux.txt')

with open(output_file, 'w') as f:
    for code in all_codes:
        f.write(code + "\n")

print(f"Postal codes have been written to {output_file}")
print("Voila bg!")
