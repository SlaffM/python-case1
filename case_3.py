from collections import defaultdict
import csv
from datetime import datetime, timedelta

registrations = {}
with open('registrations.csv', newline='', encoding='utf-8') as reg_file:
  reader = csv.DictReader(reg_file, delimiter=';')
  for item in reader:
    user_id = item['user_id']
    reg_date = datetime.strptime(item['registration_date'], "%Y-%m-%d").date()    
    registrations[user_id] = reg_date

jan_registrations = {}
for u_id, reg_date in registrations.items():
  if reg_date.month == 1:
      jan_registrations[u_id] = reg_date

logins = defaultdict(list)
logins_by_day = defaultdict(set)
with open('entries.csv', newline='', encoding='utf-8') as logins_file:
  reader = csv.DictReader(logins_file, delimiter=';')
  for item in reader:
    user_id = item['user_id']
    login_date = datetime.strptime(item['entry_date'], "%Y-%m-%d").date()

    if user_id not in registrations:
      continue  

    if user_id not in logins:
      logins[user_id] = set()
    logins[user_id].add(login_date)
    logins_by_day[login_date].add(user_id)    

logins_by_month = defaultdict(set)
for day, u_ids in logins_by_day.items():
  key = (day.year, day.month)
  logins_by_month[key].update(u_ids)

logins_by_week = defaultdict(set)
for day, u_ids in logins_by_day.items():
  iso_data = day.isocalendar()
  key = (iso_data.year, iso_data.week)
  logins_by_week[key].update(u_ids)

all_logins_days = sorted(logins_by_day.keys())
all_logins_months = sorted(logins_by_month.keys())
all_logins_weeks = sorted(logins_by_week.keys())

cohort_size = len(jan_registrations)
total_users = len(registrations)

def get_retention(n_day):
  cnt_retained_users = 0
  for id, reg_date in jan_registrations.items():
    target_date = reg_date + timedelta(days=n_day)
    user_logins = logins.get(id, set())
    if target_date in user_logins:
      cnt_retained_users += 1
  result = cnt_retained_users / cohort_size * 100 if cohort_size > 0 else 0
  return round(result,5)

def get_rolling_retention(n_day):
  cnt_reteined_users = 0
  for id, reg_date in jan_registrations.items():
    target_date = reg_date + timedelta(days=n_day)
    user_logins = logins.get(id, set())
    if any(login >= target_date for login in user_logins):
      cnt_reteined_users += 1
  result = cnt_reteined_users / cohort_size * 100 if cohort_size > 0 else 0
  return round(result,5)

def get_lifetime(max_days):  
  lifetime = 0.0
  for n in range(1, max_days):
    day_n = n - 1
    retained = 0

    for u, reg_date in registrations.items():
      target_date = reg_date + timedelta(days=day_n)
      if target_date in logins[u]:
        retained += 1
    r_n = retained / total_users
    lifetime += r_n
  return round(lifetime,5)

def get_rolling_retention_churn(n_day):
  cnt_retained_users = 0
  for id, reg_date in registrations.items():
    target_date = reg_date + timedelta(days=n_day)
    user_logins = logins.get(id, set())
    for login in user_logins:
      if login >= target_date:
        cnt_retained_users += 1
        break

  result = cnt_retained_users / total_users if total_users > 0 else 0
  return round(result,5)

def get_dec_mau(end_date):
  uniq_users = set()
  month_start = end_date - timedelta(days=30)
  for u_id, u_logins in logins.items():
    for login_date in u_logins:
      if login_date >= month_start and login_date <= end_date:
        uniq_users.add(u_id)
        break
  return len(uniq_users)

def get_dec_wau(end_date):
  uniq_users = set()
  week_start = end_date - timedelta(days=6)
  for u_id, u_logins in logins.items():
    for login_date in u_logins:
      if login_date >= week_start and login_date <= end_date:
        uniq_users.add(u_id)
        break
  return len(uniq_users)

def get_dec_dau(end_date):
  uniq_users = set()
  day_start = end_date
  for u_id, u_logins in logins.items():
    for login_date in u_logins:
      if login_date >= day_start and login_date <= end_date:
        uniq_users.add(u_id)
        break
  return len(uniq_users)

def get_avg_mau():
  mau_values = []
  for month in all_logins_months:
    mau = len(logins_by_month.get(month, set()))      
    mau_values.append(mau)
  avg_mau = sum(mau_values) / len(mau_values) if mau_values else 0
  return round(avg_mau,5)

def get_avg_wau():
  wau_values = []
  for week in all_logins_weeks:
    wau = len(logins_by_week.get(week, set()))      
    wau_values.append(wau)
  avg_wau = sum(wau_values) / len(wau_values) if wau_values else 0
  return round(avg_wau,5)

def get_avg_dau():
  dau_values = []
  for day in all_logins_days:
    dau = len(logins_by_day.get(day, set()))      
    dau_values.append(dau)
  avg_dau = sum(dau_values) / len(dau_values) if dau_values else 0
  return round(avg_dau,5)

retention_15_day = get_retention(15)
rolling_retention = get_rolling_retention(30)
lifetime = get_lifetime(max_days=90)
churn_29 = 1 - get_rolling_retention_churn(29)

end_date = datetime(2021, 12, 31).date()
dec_mau = get_dec_mau(end_date)
dec_wau = get_dec_wau(end_date)
dec_dau = get_dec_dau(end_date)
avg_mau = get_avg_mau()
avg_wau = get_avg_wau()
avg_dau = get_avg_dau()
