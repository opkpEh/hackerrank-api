from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


def scrape_hackerrank_profile(username):
    url = f"https://www.hackerrank.com/profile/{username}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Connection': 'keep-alive'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract badges (stars)
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

        # Extract certificates
        certificates_div = soup.find("div", class_="hacker-certificates")
        certificates = []
        if certificates_div:
            certificate_links = certificates_div.find_all("a", class_="certificate-link")
            for cert in certificate_links:
                cert_heading = cert.find("h2", class_="certificate_v3-heading")
                if cert_heading:
                    # Remove "Certificate: " text if present
                    cert_name = cert_heading.text.replace("Certificate:", "").strip()
                    cert_url = "https://www.hackerrank.com" + cert.get("href", "")
                    is_verified = bool(cert.find("span", class_="certificate_v3-heading-verified"))
                    certificates.append({
                        "name": cert_name,
                        "url": cert_url,
                        "verified": is_verified
                    })

        return {
            "badges": badges,
            "certificates": certificates
        }

    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error scraping profile: {str(e)}")
        return {"error": str(e)}


@app.route('/')
def home():
    return "HackerRank Profile Scraper API"


@app.route('/profile/<username>')
def get_profile(username):
    try:
        profile_data = scrape_hackerrank_profile(username)
        return jsonify(profile_data)
    except Exception as e:
        app.logger.error(f"Error processing request: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    app.run(debug=True)