import flask
from flask import render_template
from flask import Flask
from bs4 import BeautifulSoup
import requests
import time
from random import randint
from flask import request

app = Flask(__name__)

class Scrape():
    def __init__(self, limit, keyword):
        
        self.limit = limit
        self.keyword = keyword
        print("Connecting...")
        time.sleep(5)  
        self.r = requests.get("https://news.google.com/search?q={}&hl=en-PH&gl=PH&ceid=PH%3Aen".format(self.keyword))
        if self.r.status_code == 200:
            print("Connected")
        else:
            print("Failed to Connect")

    def process(self):

        content = self.r.text
        news_summaries = []
        soup = BeautifulSoup(content, "html.parser")
        st_divs = soup.findAll("div", {"class": "NiLAwe y6IFtc R7GTQ keNKEd j7vNaf"}, limit= self.limit)
        for st_div in st_divs:
            news_summaries.append(st_div.text)
        return news_summaries
    
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/process', methods=['POST', 'GET'])
def process():
    if request.method == 'POST':
        print(request.form)
        scrape_news = Scrape(int(request.form['limit']), request.form['searchbar']).process()
        headlines = [news for news in scrape_news]
        print(headlines)
        
    return render_template('home.html', headline=headlines)

if __name__ == '__main__':
    app.run(port=5000, debug=True)