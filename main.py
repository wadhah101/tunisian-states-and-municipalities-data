from bs4 import BeautifulSoup
from flask import Flask
app = Flask(__name__)


def scrape_to_variable():
    states = []
    municipalities = []
    soup = BeautifulSoup(open("data.html"), features="lxml")
    for i in soup.find_all('a'):
        title = i.get('title').replace('Le ', '').replace('La ', '').replace(
            ', Tunisia', '').replace('(municipality)', '').strip()

        if title.find('Governorate') != -1:
            name = title.replace('Governorate', '').strip()
            states.append({'name': name, 'code': len(states) + 1})
        else:
            municipalities.append({'name': title, 'gov_code': len(states)})
    return states,  municipalities


@app.route('/')
def hello_world():
    states, municipalities = scrape_to_variable()
    return {"data": {"states": states, "municipalities": municipalities}}
