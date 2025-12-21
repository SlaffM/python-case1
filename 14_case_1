from datetime import datetime as dt
def prepearing_data(logfile):
  headers = ['type', 'date', 'file', 'line', 'message']
  dict_lines = []
  with open(logfile, 'r', encoding='utf-8') as f:
    all_lines = f.readlines()
    dict_lines = [
        { k: val.strip() for k, val in zip(headers, line.split('|')) }
        for line in all_lines
    ]
  return dict_lines

lines = prepearing_data('auto_purchase.log')
lines

#Задача 1

def count_success_and_failure(dict_lines):
    attempts = list(filter(
        lambda k: 'Обновляем подписку' in k['message'], dict_lines
    ))
    err_attempts = list(filter(
        lambda k: k['type'].lower()=='error', dict_lines
    ))
    count_success_attempts = len(attempts) - len(err_attempts)
    count_error_attempts = len(err_attempts)

    return (count_success_attempts, count_error_attempts)

count_success_and_failure = count_success_and_failure(lines)
count_success_and_failure

#Задача 2

import re
from collections import defaultdict

def get_stat():
  users_by_days_source = defaultdict(list)
  for el in lines:
    renewal_date = (el['date'][:10])
    pattern = r"автопродлением подписки: (\d+$)"
    match = re.search(pattern=pattern, string=el['message'])
    if match:
      users_by_days_source[renewal_date].append(int(match.group(1)))
  users_by_days = [
      (k, max(v))
      for k, v in users_by_days_source.items()
  ]
  return users_by_days

def calc_median(lst):
  sorted_lst = sorted(lst)
  num = len(sorted_lst)
  if num % 2 == 1:
    return sorted_lst[num // 2]
  else:
    num1 = sorted_lst[num // 2 - 1]
    num2 = sorted_lst[num // 2]
    return int(round((num1 + num2) / 2, 0))

def auto_renewal_sub(log_file_path):
  lines = prepearing_data(log_file_path)
  users_by_days = get_stat()

  values = [ d[1] for d in users_by_days ]
  res_avg = []
  res_med = []
  for i in range(len(users_by_days)):
    window_values = values[0:i+1]

    avg = sum(window_values) / len(window_values)
    res_avg.append(round(avg,2))

    median = calc_median(window_values)
    res_med.append(median)

  with open('auto_renewal_sub.txt', 'w', encoding='utf-8') as f:
    f.writelines(f'Среднее: {res_avg}\n')
    f.writelines(f'Медиана: {res_med}')

auto_renewal_sub('auto_purchase.log')

#Задача 3

from collections import defaultdict

def sub_renewal_by_day(log_file_path):
  lines = prepearing_data(log_file_path)
  weekdays = [
      'Понедельник', 
      'Вторник',
      'Среда',
      'Четверг',
      'Пятница',
      'Суббота',
      'Воскресенье'
  ]
  subs = defaultdict(int)

  for line in lines:
    weekday = dt.fromisoformat(line['date']).isoweekday()
    if 'Обновляем подписку пользователю' in line['message']:
      subs[weekday] += 1

    if 'ошибка при списании' in line['message']:
      subs[weekday] -= 1

  with open('weekdays.txt', 'w', encoding='utf-8') as f:
    f.write(f'Количество обновлений подписки по дням недели:\n')
    f.writelines(
        f'{day}: {subs[i]}\n' if i < len(weekdays) else f'{day}: {subs[i]}' 
        for i, day in enumerate(weekdays, 1) 
    )
  
sub_renewal_by_day('auto_purchase.log')
