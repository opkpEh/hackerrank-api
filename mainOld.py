from scrapingbee import ScrapingBeeClient

client = ScrapingBeeClient(api_key="USBUIIJHJV26FF2005DNO41JLS4AL1VWU2GRSSADJMA61G8M1QAZNDADPT46175XWH4RO79GD7JH07KG")

response = client.get(
    "https://www.hackerrank.com/kp2598/hackos",
    params={
        'premium_proxy': True,
        'country_code': 'gb',
        "block_resources": False,
        'device': 'desktop',
        "wait": "2000",
        "render_js": "True",
    },
    headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.hackerrank.com/profile/kp2598"
    },
    cookies={
    },
)

print(response.content)
