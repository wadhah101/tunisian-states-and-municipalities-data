from bs4 import BeautifulSoup
from collections import defaultdict
import mysql.connector as mysql
import json

states = []
municipalities = []


def scrape_to_variable():
    soup = BeautifulSoup(open("data.html"), features="lxml")
    for i in soup.find_all('a'):
        title = i.get('title')
        title = title.replace('Le ', '')
        title = title.replace('La ', '')
        title = title.replace(', Tunisia', '')
        title = title.replace('(municipality)', '')
        title = title.strip()
        # print(title)
        if title.find('Governorate') != -1:
            name = title.replace('Governorate', '').strip()
            states.append({'name': name, 'id': len(states) + 1})
        else:
            municipalities.append({'name': title, 'id': len(municipalities) + 1, 'gouv_id': len(states)})


def write_to_json():
    if len(states) == 0:
        raise OSError('please use scrape_to_variable() first')

    with open('output/municipalities.json', 'w') as json_file:
        json.dump(municipalities, json_file, indent=2)

    with open('output/states.json', 'w') as json_file:
        json.dump(states, json_file, indent=2)


def insert_into_db():
    if len(states) == 0:
        raise OSError('please use scrape_to_variable() first')

    db = mysql.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="covoiturage"
    )
    cursor = db.cursor()

    for i in states:
        query = "INSERT INTO gouvernorat (id, name) VALUES (%s,%s)"
        value = (i['id'], i['name'])
        cursor.execute(query, value)

    for i in municipalities:
        query = "INSERT INTO ville(id,name,gouv_id) VALUES (%s,%s,%s)"
        value = i['id'], i['name'], i['gouv_id']
        cursor.execute(query, value)

    db.commit()


if __name__ == '__main__':
    # should always be called
    scrape_to_variable()

    # write output to json
    write_to_json()
    # insert_into_db()
