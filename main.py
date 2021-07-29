import os
import string
import ntpath
import datetime
from pprint import pprint
import json


def get_rows(filename):
    month_name_year = ntpath.basename(filename).replace('.csv', '').replace('Uscite_', '')
    year_month = month_name_year.split('_')[1] + '-' + str(f"{datetime.datetime.strptime(month_name_year.split('_')[0], '%B').month:02}")

    rows = []
    with open(filename, 'r', encoding="utf-8") as input_file:
        lines = input_file.readlines()[1:]
        for line in lines:
            line = line.split('",')
            line[0] = ''.join([char for char in line[0].replace('"', '').replace("'", '').lower().replace(' ', '_') if char in set(string.ascii_lowercase + '&')]).replace('&', '_and_')
            line[1] = float(line[1].replace('-€', '').replace("\n", '').replace('"', '').replace(' ', '').replace('.', '').replace(',', '.'))
            rows.append(line)
        return year_month, rows


if __name__ == "__main__":
    year_month_data = {}

    for filename in os.listdir('./inputfiles/'):
        year_month, rows = get_rows(f'./inputfiles/{filename}')
        year_month_data[year_month] = {
            'categories': rows,
            'total': sum([row[1] for row in rows])
        }
    
    json_repr = json.dumps(year_month_data, sort_keys=True, indent=4)
    with open('export.json', 'w') as output_file:
        output_file.write(json_repr)
