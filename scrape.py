import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def fetch_onion_site_html(url, session):
    try:
        response = session.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.text
    except requests.RequestException as e:
        return f"Error fetching {url}: {e}"

def save_html(content, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Saved HTML content to {path}")

def is_valid_link(url, domain):
    # Check if the link is valid and belongs to the same domain
    return urlparse(url).netloc == domain

def scrape_site(url, session, base_path):
    domain = urlparse(url).netloc
    visited = set()
    to_visit = [url]

    while to_visit:
        current_url = to_visit.pop(0)
        if current_url in visited:
            continue
        visited.add(current_url)

        html_content = fetch_onion_site_html(current_url, session)
        if "Error fetching" in html_content:
            continue

        # Save the current page
        page_filename = os.path.join(base_path, urlparse(current_url).path.strip('/').replace('/', '_') or 'index.html')
        save_html(html_content, page_filename)

        # Parse the page to find links
        soup = BeautifulSoup(html_content, 'html.parser')
        for link in soup.find_all('a', href=True):
            full_link = urljoin(current_url, link['href'])
            if is_valid_link(full_link, domain) and full_link not in visited:
                to_visit.append(full_link)

# Main execution setup
if __name__ == "__main__":
    urls = [
    "http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/", #DuckDuckGo 
    "http://haystak5njsmn2hqkewecpaxetahtwhsbsa64jom2k22z5afxhnpxfid.onion/", #Haystak
    "http://xmh57jrknzkhv6y3ls3ubitzfqnkrwxhopf5aygthi7d6rplyvk3noyd.onion/" #Hej
]

    session = requests.session()
    session.proxies = {'http': 'socks5h://localhost:9050', 'https': 'socks5h://localhost:9050'}

    for url in urls:
        base_directory = f"onion_sites_html/{urlparse(url).netloc}"
        scrape_site(url, session, base_directory)
