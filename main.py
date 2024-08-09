import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin

def fetch_website(url):
    """Fetches the HTML content and measures page load time."""
    start_time = time.time()
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None, None
    end_time = time.time()
    load_time = end_time - start_time
    return response.text, load_time

def analyze_resources(html_content, base_url):
    """Analyzes the size of resources like CSS, JavaScript, and images."""
    soup = BeautifulSoup(html_content, 'html.parser')
    resources = {'css': [], 'js': [], 'img': []}

    # Extract CSS links
    for link in soup.find_all('link', rel='stylesheet'):
        href = link.get('href')
        if href:
            resources['css'].append(urljoin(base_url, href))

    # Extract JavaScript files
    for script in soup.find_all('script'):
        src = script.get('src')
        if src:
            resources['js'].append(urljoin(base_url, src))

    # Extract image sources
    for img in soup.find_all('img'):
        src = img.get('src')
        if src:
            resources['img'].append(urljoin(base_url, src))

    return resources

def measure_resource_size(urls):
    """Measures the size of resources by making HTTP requests."""
    sizes = {'css': 0, 'js': 0, 'img': 0}

    for category, urls_list in urls.items():
        for url in urls_list:
            try:
                response = requests.get(url)
                sizes[category] += len(response.content)
            except requests.RequestException as e:
                print(f"Error fetching {url}: {e}")

    return sizes

def generate_report(url, load_time, resources, sizes):
    """Generates a performance report."""
    total_size = sum(sizes.values())
    num_resources = sum(len(urls) for urls in resources.values())

    print(f"\nURL: {url}")
    print(f"Page Load Time: {load_time:.2f} seconds")
    print(f"Total Page Size: {total_size / 1024:.2f} KB")
    print(f"Number of Resources: {num_resources}")
    print(f"CSS Size: {sizes['css'] / 1024:.2f} KB")
    print(f"JS Size: {sizes['js'] / 1024:.2f} KB")
    print(f"Image Size: {sizes['img'] / 1024:.2f} KB")

def main():
    # Prompt the user to enter the URL
    url = input("Enter the URL of the site to analyze: ").strip()
    if not url.startswith('http'):
        url = 'http://' + url

    html_content, load_time = fetch_website(url)
    if html_content is None:
        return

    # Use the base URL for resolving relative resource URLs
    base_url = url if url.endswith('/') else url + '/'
    resources = analyze_resources(html_content, base_url)
    sizes = measure_resource_size(resources)
    generate_report(url, load_time, resources, sizes)

if __name__ == "__main__":
    main()
