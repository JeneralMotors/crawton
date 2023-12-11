import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def get_links(url, target_domain):
    try:
        # Add a User-Agent to simulate a real browser
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        
        # Make an HTTP request and parse the content with BeautifulSoup
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get links and ensure they are absolute URLs belonging to the same domain
        parsed_target = urlparse(target_domain)
        return [urljoin(url, a['href']) for a in soup.find_all('a', href=True)
                if urlparse(urljoin(url, a['href'])).netloc == parsed_target.netloc]
    except requests.exceptions.RequestException as e:
        # Handle specific HTTP request errors
        print(f"HTTP request error while getting links from {url}: {e}")
        return []
    except Exception as e:
        # Handle other errors
        print(f"Error getting links from {url}: {e}")
        return []

def scrape_recursive(url, depth, target_domain):
    visited_links = set()

    def scrape(url, current_depth):
        if current_depth > depth or url in visited_links:
            return
        
        # Mark the URL as visited and display information
        visited_links.add(url)
        print(f"Processing link (Depth {current_depth}): {url}")

        # Get links from the current URL and recursively scrape
        links = get_links(url, target_domain)
        for link in links:
            scrape(link, current_depth + 1)
            # Add a small delay between requests to be server-friendly
            time.sleep(0.5)

    scrape(url, 1)

if __name__ == "__main__":
    try:
        # Prompt the user for the target URL and maximum depth
        target_url = input("Enter the target URL (scope): ").strip()
        depth = int(input("Enter the maximum scraping depth: ").strip())

        # Validate user input
        if not target_url.startswith(('http://', 'https://')):
            raise ValueError("URL must start with 'http://' or 'https://'")

        # Start recursive scraping with the concept of "scope"
        scrape_recursive(target_url, depth, target_url)

    except ValueError as ve:
        print(f"Error: {ve}")
    except KeyboardInterrupt:
        print("\nProcess interrupted by the user.")
    except Exception as e:
        print(f"Unexpected error: {e}")
