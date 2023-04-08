import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import time
import json


def get_headers():
    return Headers(browser='chrome', os='win').generate()


def switch_page(params):
    print(f'Парсим страницу {params["page"]}')
    params['page'] += 1
    return params


def pars_hh():
    vacancys_data = []
    url = 'https://hh.ru/search/vacancy'
    params = {'text': 'python django flask',
              'area': [1, 2],
              'page': 0,
              'items_on_page': 20
              }
    try:
        while True:
            time.sleep(0.003)
            response = requests.get(url=url, headers=get_headers(), params=params)
            soup = BeautifulSoup(response.text, 'lxml')
            switch_page(params)
            vacancys_div = soup.find('div', id='a11y-main-content')
            vacancys = vacancys_div.find_all('div', class_='serp-item')
            for vacancy in vacancys:
                vacancy_name = vacancy.find('h3')
                vacancy_link = vacancy_name.find('a').attrs['href']

                try:
                    vacancy_salary = vacancy.find('span', class_='bloko-header-section-3').text.replace('\u202f', ' ')
                except:
                    vacancy_salary = 'Не указана'
                vacancy_company = vacancy.find('div', class_='vacancy-serp-item__meta-info-company').text
                vacancy_placement = vacancy.find('div', class_="vacancy-serp-item__info").contents[1].contents[0]
                vacancys_data.append({
                            'Должность': vacancy_name.text.replace('000\ха', ''),
                            'Ссылка на вакансию': vacancy_link,
                            'Зарплата': vacancy_salary,
                            'Компания': vacancy_company,
                            'Территориальное расположение': vacancy_placement
                        })

    except Exception:
        print('Все вакансии прочитаны')
        print(f'Успешно добавленно {len(vacancys_data)} вакансий')
        return vacancys_data


if __name__ == "__main__":
    with open('all_vacancys.json', 'w', encoding='utf-8') as f:
        json.dump(pars_hh(), f, ensure_ascii=False, indent=5)
