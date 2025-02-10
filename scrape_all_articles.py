import time
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By

# Import the article scraper function
from substack_scraper import scrape_substack_article
from date_selector import get_user_date

def scrape_author_page(author_url):
    # Get the date directly inside this function (no more min_date argument).
    min_date = get_user_date()  

    # Initiate Chrome driver
    driver = webdriver.Chrome()
    
    valid_articles = []

    try:
        driver.get(author_url)
        time.sleep(5)

        # Find article links (Substack article links contain "/p/")
        anchor_elems = driver.find_elements(By.CSS_SELECTOR, "a[href*='/p/']")
        article_links = []

        for elem in anchor_elems:
            href = elem.get_attribute("href")
            if href:
                # Build the individual article URLs correctly
                if not href.startswith("http"):
                    if '/@' in author_url:
                        username = author_url.split('/@')[1].strip('/')
                        base_url = f"https://{username}.substack.com"
                        href = base_url + href
                    else:
                        href = urllib.parse.urljoin(author_url, href)

                if href not in article_links:
                    article_links.append(href)

        print(f"Found {len(article_links)} articles. Now filtering by date...")

        # Scrape each article and filter by the chosen date
        for article_url in article_links:
            article_data = scrape_substack_article(article_url, min_date)
            if article_data:
                valid_articles.append(article_data)
                print(f"✔ Article '{article_data['Article_Title']}' from {article_data['Article_Posted_Date']} meets the date requirement.")
            else:
                print("⚠ Encountered an article that does not meet the date requirement. Stopping further scraping.")
                break  # EARLY TERMINATION once we hit older content

    finally:
        driver.quit()

    return valid_articles

# Tester main function
def main():
    test_url = "https://substack.com/@cryptohayes"

    articles = scrape_author_page(test_url)

    print("Final List of Articles Meeting the Date Criteria:")
    for article in articles:
        print(f"- {article['Article_Title']} (Published: {article['Article_Posted_Date']})")

if __name__ == "__main__":
    main()
