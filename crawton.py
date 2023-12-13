import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from multiprocessing import Pool
import time
import random

def get_links(url_target_domain):
    """
    Retrieve links from a given URL within the specified target domain.

    :param url_target_domain: Tuple containing the URL and the target domain.
    :return: List of tuples containing the absolute URLs and target domains of the links.
    """
    url, target_domain = url_target_domain
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        parsed_target = urlparse(target_domain)
        # Extract absolute URLs with the same target domain
        return [(urljoin(url, a['href']), target_domain) for a in soup.find_all('a', href=True)
                if urlparse(urljoin(url, a['href'])).netloc == parsed_target.netloc]
    except requests.exceptions.RequestException as e:
        print(f"HTTP request error while getting links from {url}: {e}")
        return []
    except Exception as e:
        print(f"Error getting links from {url}: {e}")
        return []

def scrape_recursive(args):
    """
    Recursively scrape links up to a specified depth.

    :param args: Tuple containing the URL, depth, and target domain.
    """
    url, depth, target_domain = args
    visited_links = set()

    def scrape(url, current_depth):
        if current_depth > depth or url in visited_links:
            return

        visited_links.add(url)
        print(f"Processing link (Depth {current_depth}): {url}")

        links = get_links((url, target_domain))
        for link, _ in links:
            scrape(link, current_depth + 1)
            # Add a random wait time between 0.50 and 0.97 seconds
            time.sleep(random.uniform(0.50, 0.97))

    scrape(url, 1)

if __name__ == "__main__":
    try:
        target_url = input("Enter the target URL (scope): ").strip()
        depth = int(input("Enter the maximum scraping depth: ").strip())

        if not target_url.startswith(('http://', 'https://')):
            raise ValueError("URL must start with 'http://' or 'https://'")

        # Use multiprocessing Pool
        pool = Pool()
        pool.map(scrape_recursive, [(target_url, depth, target_url)])
        pool.close()
        pool.join()

    except ValueError as ve:
        print(f"Error: {ve}")
    except KeyboardInterrupt:
        print("\nProcess interrupted by the user.")
    except Exception as e:
        print(f"Unexpected error: {e}")
