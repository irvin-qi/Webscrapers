import time
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By

# Scraping function to scrape an individual article
from substack_scraper import scrape_substack_article

def scrape_author_page(author_url):
    # Initiate Chrome driver
    driver = webdriver.Chrome()
    # List stores all articles urls to be parsed by individual article scraper
    article_links = []

    try:
        driver.get(author_url)
        # Delay to load page
        time.sleep(3)  

        # Links to an author's articles are always <a> tags with an href containing "/p/"
        anchor_elems = driver.find_elements(By.CSS_SELECTOR, "a[href*='/p/']")
        
        for elem in anchor_elems:
            href = elem.get_attribute("href")
            if href:
                # Build the individual article URLs from landing page https://substack.com/@{username}
                if not href.startswith("http"):
                    # Extract the username by splitting the URL at '/@'
                    if '/@' in author_url:
                        username = author_url.split('/@')[1].strip('/')
                        base_url = f"https://{username}.substack.com"
                        # Add back each article name to the base URL to achieve format: "https://{username}.substack.com/p/{article-name}"
                        href = base_url + href
                    else:
                        href = urllib.parse.urljoin(author_url, href)
                # Add the URL to the list of individual article links
                if href not in article_links:
                    article_links.append(href)
                    
    finally:
        driver.quit()

    return article_links
