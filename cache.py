import requests
import sqlite3
import datetime
from time import sleep

def update_all_data():
    all_departements = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','2A','2B','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','62','63','64','65','66','67','68','69','70','71','72','73','74','75','76','77','78','79','80','81','82','83','84','85','86','87','88','89','90','91','92','93','94','95','971','972','973','974','975','976','977','978','986','987','988']
    today = datetime.date.today()

    for dep in all_departements:
        response = requests.get(f"https://geo.api.gouv.fr/departements/{dep}/communes")
        data = response.json()
        dep_codes = [','.join(commune.get('codesPostaux', [])) for commune in data]
        
        conn = sqlite3.connect('cache.db')
        c = conn.cursor()
        c.execute("REPLACE INTO codes_postaux (departement, codes, derniere_mise_a_jour) VALUES (?, ?, ?)", 
                  (dep, ','.join(dep_codes), today))
        conn.commit()
        conn.close()

if __name__ == "__main__":
    update_all_data()
