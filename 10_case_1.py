from glob import glob
import re
import csv

def process_files(src_folder, dest_folder):
  headers = []
  good_files = []

  for file in glob(f'{src_folder}/*.csv'):
    match_template = re.search(r'\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d+.csv', file)
    if match_template:
      good_files.append(file)

  required_headers = ['date', 'product', 'store', 'cost']
  data = []

  for f_elem in good_files:
    with open(f_elem) as f:
      reader = csv.reader(f, delimiter=';')
      raw_rows = list(reader)  

      raw_cols = []
      for h in raw_rows[0]:        
        raw_cols.append(h.lower())
      
      norm_headers = {}
      for raw_row in raw_rows[1:]:        
        sel_headers = {}
        for key, value in zip(raw_cols, raw_row):
          norm_headers[key] = value

        for header in required_headers:
          sel_headers[header] = norm_headers.get(header, '')

        data.append(list(sel_headers.values()))   

  data.sort(key=sort_key)

  data.insert(0, required_headers)

  with open(f'{dest_folder}/combined_data.csv', 'w') as fw:
    writer = csv.writer(fw, delimiter=',')
    writer.writerows(data)

def sort_key(row):
  return (row[0], row[1])
