import gspread
from oauth2client.service_account import ServiceAccountCredentials

def generate_report(sheet1,sheet2,sheet3):
  scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']

  creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

  client = gspread.authorize(creds) 

  sheet1 = client.open('Installments').worksheet(sheet1)
  sheet1_data = sheet1.get_all_records()
  sheet2 = client.open('Installments').worksheet(sheet2)
  sheet2_data = sheet2.get_all_records()
  sheet3 = client.open('Installments').worksheet(sheet3)
  sheet3_data = sheet3.get_all_records()
  return sheet1_data, sheet2_data, sheet3_data 

sheet1_data, sheet2_data, sheet3_data = generate_report("Лист1","Лист2","Лист3")

import math
from datetime import datetime as dt

PAYMENT_PERIOD = 183
END_PAYMENT_DAY = dt.fromisoformat(f'2023-03-01')


def calc_dolg(student_rec): 
  expected_date = dt.strptime(student_rec['expected_payment_date'], "%d.%m.%Y")

  if expected_date >= END_PAYMENT_DAY:
    return 0

  over_days = (END_PAYMENT_DAY - expected_date).days

  cnt_periods = 0
  if over_days > 0:
    cnt_periods = math.ceil(over_days / PAYMENT_PERIOD)  

  calculated_dolg = student_rec['one-time_payment'] * cnt_periods

  return min(calculated_dolg, student_rec['left_to_pay'])


students_installments= [st for st in sheet1_data if st['installment']=='Y']
students_data = []

for st, st_dates, st_payments in zip(students_installments, sheet2_data, sheet3_data):
  student_info = {**st, **st_dates, **st_payments}
  
  dolg = calc_dolg(student_info)

  if dolg > 0:
    students_data.append((student_info['student_id'], student_info['student_name'], dolg)) 

if not students_data:
  text_lines = []
else:
  text_lines = [
      f"Студент {name} - долг {dolg} рублей"
      for id, name, dolg in students_data
  ]  

with open('student_debt_report.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(text_lines))
