import csv
from collections import defaultdict
from datetime import date, timedelta


def get_platform_city_results():
  platforms = defaultdict(dict)

  for el in elements:

    platform = el.get('Платформа')
    town = el.get('Город')
    expenses = float(el.get('Бюджет'))

    if town not in platforms[platform]:
        platforms[platform][town] = 0.0

    platforms[platform][town] += expenses

  calc_towns = {}
  for platform, cities in platforms.items():    
    total = sum(cities.values())
    if total == 0:
      calc_towns[platform] = {city: 0.0 for city in cities}
    else:
      calc_towns[platform] = {
        city: round(expenses / total * 100, 2)
        for city, expenses in cities.items()
      }

  sorted_towns = {
      platform : dict(sorted(cities.items(), key=lambda city : city[1], reverse=True))
      for platform, cities in calc_towns.items()
  }

  return sorted_towns

res = get_platform_city_results()
res

with open('platform_city_results.txt', 'w', encoding='utf-8') as f:
  for platform, cities in res.items():
    f.write(f'Для группы {platform}:\n')
    for city, expenses in cities.items():
      f.write(f'- Город: {city}, доля затрат на рекламу: {expenses}%\n')


def calculate_average_budget(file, filter):
  elements = []
  with open(file, newline='', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file)
    for el in reader:
      elements.append(el)      

  parameters = dict()

  for el in elements:

    parameter = el.get('Платформа')

    if parameter not in filter:
      continue

    budget = float(el.get('Бюджет'))

    if parameter in parameters:
      parameters[parameter][0] += budget
      parameters[parameter][1] += 1
    else:
      parameters[parameter] = [budget, 1]

  

  result = round(parameters[filter][0] / parameters[filter][1], 2)
  return result



def get_missing_campaign_dates(file):

  start_date = date(2022,1,1)
  end_date = date(2022,12,31)
  days = (end_date - start_date).days
  gen_dates = set(start_date + timedelta(days=i) for i in range(days))

  elements = []
  with open(file, newline='', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file)
    for el in reader:
      elements.append(el)      

  parameters = set()

  for el in elements:
    parameter = el.get('Начальная дата')
    parameters.add(datetime.strptime(parameter, '%Y-%m-%d').date())

  imported_dates = set(sorted(parameters))
  result = list(gen_dates.difference(imported_dates))
  result.sort()

  for item in result:
    yield item


def group_campaign_data(file):
  elements = []
  with open(file, newline='', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file)
    for el in reader:
      elements.append(el)      

  parameters = dict()

  for el in elements:

    parameter = el.get('Город')
    budget = int(el.get('Бюджет'))
    clicks = float(el.get('Клики'))

    if parameter in parameters:
      parameters[parameter][0] += clicks
      parameters[parameter][1] += budget
    else:
      parameters[parameter] = [clicks, budget]

  sorted_data = dict(sorted(parameters.items()))

  output_data = [
      {
          'Город': town,
          'Количество кликов': props[0],
          'Суммарный бюджет':props[1],
      }
      for town, props in sorted_data.items()
  ]
  return output_data


def campaign_generator(file, town, budget):
  elements = []
  with open(file, newline='', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file)
    for el in reader:
      elements.append(el)

  cities = list()

  for el in elements:

    city = el.get('Город')

    if city != town:
      continue   
    
    budget_company = int(el.get('Бюджет'))
      
    if budget_company <= int(budget):
      continue

    id_company = el.get('ID Кампании')
    type_company = el.get('Тип кампании')
    platform = el.get('Платформа')
    dohod = el.get('Доход')
      
    city = {}
    city['ID Кампании'] = id_company
    city['Тип'] = type_company
    city['Платформа'] = platform
    city['Доход'] = dohod
    cities.append(city) 

  sorted_data = sorted(cities, key=lambda x : int(x['ID Кампании']))

  for item in sorted_data:
    yield item  




