import time
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime

try:
    import tkinter as tk
    from tkcalendar import Calendar
    GUI_ENABLED = True  # If tkinter loads successfully, enable GUI mode
except ImportError:
    print("⚠ GUI mode unavailable. Using hardcoded date: 2025-01-01")
    GUI_ENABLED = False  # Disable GUI if Tkinter is not available

# Import the article scraper function
from substack_scraper import scrape_substack_article


def get_user_date():
    """
    Opens a calendar-based date selector GUI. If GUI fails, defaults to "2025-01-01".
    
    :return: Date string in 'YYYY-MM-DD' format
    """
    default_date = "2025-01-01"

    if GUI_ENABLED:
        try:
            # Initialize the selected_date variable outside of set_date function
            selected_date = None

            # Create a pop-up window
            root = tk.Tk()
            root.withdraw()  # Hide main window
            
            # Create a second window for date selection
            date_window = tk.Toplevel(root)
            date_window.title("Select Minimum Article Date")
            date_window.geometry("400x300")

            # Calendar widget
            cal = Calendar(date_window, selectmode="day", year=2025, month=1, day=1)
            cal.pack(pady=20)

            # Function to set selected date and close window
            def set_date():
                nonlocal selected_date  # Ensure the function modifies the outer variable
                selected_date = cal.get_date()  # Format: M/D/YY or MM/DD/YYYY
                date_window.destroy()

            # Button to confirm date selection
            select_btn = tk.Button(date_window, text="Select Date", command=set_date)
            select_btn.pack()

            # Run the GUI and wait for user input
            root.wait_window(date_window)

            # If no date was selected, return default
            if not selected_date:
                print(f"⚠ No date selected. Using default: {default_date}")
                return default_date

            # Convert the selected date format dynamically
            try:
                parsed_date = datetime.strptime(selected_date, "%m/%d/%y")  # Handles M/D/YY
            except ValueError:
                parsed_date = datetime.strptime(selected_date, "%m/%d/%Y")  # Handles MM/DD/YYYY

            formatted_date = parsed_date.strftime("%Y-%m-%d")  # Convert to YYYY-MM-DD
            print(f"✅ Using user-selected date: {formatted_date}")
            return formatted_date

        except Exception as e:
            print(f"⚠ GUI error: {e}. Using hardcoded date: {default_date}")
            return default_date

    # If GUI is not available, return hardcoded default
    return default_date


def scrape_author_page(author_url):
    """
    Scrapes an author's Substack page for article links, then uses a user-selected date
    to filter and retrieve only newer articles. Early termination occurs if an article
    is older than the chosen date.
    
    :param author_url: The URL of the Substack author page
    :return: List of articles (title, date, body, source) that meet the date requirement
    """

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


def main():
    # Example test URL; replace with an actual Substack author page
    test_url = "https://substack.com/@cryptohayes"

    articles = scrape_author_page(test_url)

    print("\n✅ Final List of Articles Meeting the Date Criteria:")
    for article in articles:
        print(f"- {article['Article_Title']} (Published: {article['Article_Posted_Date']})")


if __name__ == "__main__":
    main()
