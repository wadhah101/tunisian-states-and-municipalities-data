from bs4 import BeautifulSoup
import json


def scrape_to_variable():
    states = []
    municipalities = []
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
            municipalities.append({'name': title, 'id': len(
                municipalities) + 1, 'gouv_id': len(states)})
    return states,  municipalities


def write_to_json(states, municipalities):
    if len(states) == 0:
        raise OSError('please use scrape_to_variable() first')

    with open('output/municipalities.json', 'w') as json_file:
        json.dump(municipalities, json_file, indent=2)

    with open('output/states.json', 'w') as json_file:
        json.dump(states, json_file, indent=2)


if __name__ == '__main__':
    # should always be called
    states, municipalities = scrape_to_variable()

    write_to_json(states, municipalities)
