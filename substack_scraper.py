from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def scrape_substack_article(article_url):

    # Using Chrome driver
    driver = webdriver.Chrome() 

    try:
        # Navigate to the article page
        driver.get(article_url)

        # Give elements time to load
        time.sleep(3)

        # Article Title
        title_element = driver.find_element(By.CSS_SELECTOR, "h1.post-title.unpublished")
        article_title = title_element.text

        # Article Body
        body_element = driver.find_element(By.CSS_SELECTOR, "div.available-content")
        article_body = body_element.text

        # Source
        article_source = article_url

        # Return the scraped data as a dictionary
        return {
            "title": article_title,
            "body": article_body,
            "source": article_source
        }

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    finally:
        driver.quit()


if __name__ == "__main__":
    # Replace with a valid Substack article URL
    url = "https://substack.com/home/post/p-155873854"

    # Scrape the article
    article_data = scrape_substack_article(url)

    if article_data:
        print("Name of the Article:", article_data["title"])
        print("Article Body:", article_data["body"])
        print("Source:", article_data["source"])
