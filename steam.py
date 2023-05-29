from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route("/")
def home():
    steam_sales = get_steam_sales()
    return render_template('sales.html', sales=steam_sales)

def get_steam_sales():
    url = "https://store.steampowered.com/search/?specials=1"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    sales = []
    
    for game_div in soup.find_all('div', class_='responsive_search_name_combined'):
        title = game_div.find('span', class_='title').text
        discount = game_div.find('div', class_='col search_discount responsive_secondrow').text.strip()
        
        price_div = game_div.find('div', class_='col search_price discounted responsive_secondrow')
        if price_div is not None:
            price_text = price_div.text.strip()
            price = price_text.split('€')[1] if '€' in price_text else 'Not available'
        else:
            price = 'Not available'
        
        image_url = game_div.parent.find('div', class_='col search_capsule').find('img')['src']
        
        sales.append({'title': title, 'discount': discount, 'price': price, 'image_url': image_url})

    return sales


if __name__ == "__main__":
    app.run(debug=True)
