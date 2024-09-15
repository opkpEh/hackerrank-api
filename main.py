from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_hackerrank_profile(username):
    url = f"https://www.hackerrank.com/profile/{username}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        'Connection':'keep-alive'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        badge_titles = soup.find_all("svg", class_="hexagon")
        
        badges = []
        for badge_title in badge_titles:
            title_element = badge_title.find("text", class_="badge-title")
            if title_element:
                title_name = title_element.text.strip()
                badge_star = badge_title.find_all("path", class_="star")
                badges.append({
                    "title": title_name,
                    "stars": len(badge_star)
                })
        
        return badges
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

@app.route('/profile/<username>')
def get_profile(username):
    badges = scrape_hackerrank_profile(username)
    return jsonify(badges)

if __name__ == '__main__':
    app.run(debug=True)
