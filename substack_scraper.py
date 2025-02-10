from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime

def scrape_substack_article(article_url, min_date):
    # Using Chrome driver
    driver = webdriver.Chrome()

    try:
        # Navigate to the article page (Initial fast load)
        driver.get(article_url)
        article_url = str(article_url)
        time.sleep(1)  # Minimal wait for initial load

        # Extract Article Date **FIRST**
        article_date_text = "Date not found"
        article_date_formatted = None

        try:
            date_element = driver.find_element(By.CSS_SELECTOR, 
                "div.pencraft.pc-reset.color-pub-secondary-text-hGQ02T.line-height-20-t4M0El.font-meta-MWBumP.size-11-NuY2Zx.weight-medium-fw81nC.transform-uppercase-yKDgcq.reset-IxiVJZ.meta-EgzBVA")

            if date_element:
                article_date_text = date_element.text.strip()
                print(f"Extracted raw date: {article_date_text}")  # Display raw date

                # Convert to datetime format using correct abbreviation format
                article_date = datetime.strptime(article_date_text, "%b %d, %Y")  # Example: "JAN 27, 2025"
                article_date_formatted = article_date.strftime("%Y-%m-%d")  # Convert to YYYY-MM-DD format
                print(f"Formatted date: {article_date_formatted}")  # Display formatted date

                # Convert min_date to datetime object
                min_date_obj = datetime.strptime(min_date, "%Y-%m-%d")

                # Check date condition **BEFORE loading the rest**
                if article_date < min_date_obj:
                    print(f"Skipping article published on {article_date_formatted} (before {min_date})")
                    return None

        except ValueError:
            print(f"Warning: Could not parse date '{article_date_text}'. Skipping article.")
            return None  # Exit early if date cannot be determined

        except Exception as e:
            print(f"Unexpected error extracting date: {e}")
            return None

        # If date is valid, wait an additional 2 seconds for the full content
        time.sleep(2)

        # Extract Article Title
        title_element = driver.find_element(By.CSS_SELECTOR, "h1.post-title.unpublished")
        article_title = title_element.text

        # Extract Article Author
        try:
            author_element = driver.find_element(By.CSS_SELECTOR, 
                "a.pencraft.pc-reset.decoration-hover-underline-ClDVRM.reset-IxiVJZ")
            article_author = author_element.text.strip().title()
        except Exception:
            article_author = "Author not found"

        # Extract Article Body
        body_element = driver.find_element(By.CSS_SELECTOR, "div.available-content")
        article_body = body_element.text

        posted_date_epoch = None
        if article_date_formatted:
            posted_date_epoch = int(datetime.strptime(article_date_formatted, "%Y-%m-%d").timestamp())

        # Construct final output
        return {
            "Article_Title": article_title,
            "Article_Author": article_author,
            "Article_Source": "Substack",  # Replace this if the source varies
            "Article_Posted_Date": posted_date_epoch,  # Seconds since epoch
            "Article_Link": article_url,
            "Article_Body": article_body,
            "Metadata": {  # Optional metadata
            }
        }

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    finally:
        driver.quit()