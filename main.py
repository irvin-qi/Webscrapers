from substack_scraper import scrape_substack_article
from scrape_all_articles import scrape_author_page
from save_to_csv import save_data

if __name__ == "__main__":
    # URL of the author's Substack page
    author_page_url = "https://substack.com/@cryptohayes/"

    # Test Url with less articles to scrape
    # author_page_url = "https://substack.com/@rajvirkohli/"

    # Call the save_data function to scrape and save the data to a CSV file
    save_data(author_page_url)
