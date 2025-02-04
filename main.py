from substack_scraper import scrape_substack_article
from scrape_all_articles import scrape_author_page

if __name__ == "__main__":
    # URL of the author's Substack page
    author_page_url = "https://substack.com/@cryptohayes/"

    # Scrape individual article URLs from the author's page
    all_article_urls = scrape_author_page(author_page_url)

    # Run the individual article scraper on each article
    for url in all_article_urls:
        print("URL:", url)
        data = scrape_substack_article(url)
        if data:
            print("Title:", data["title"])
            print("Body (truncated):", data["body"][:100], "...")
            print("Source:", data["source"])
            print("-" * 40)
