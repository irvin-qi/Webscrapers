import csv
from scrape_all_articles import scrape_author_page

def save_data(author_url):
    """
    Scrapes articles from a Substack author page and saves the data to a CSV file.
    :param author_url: URL of the Substack author's page
    """

    # Get all article data from the author's page
    all_articles = scrape_author_page(author_url)

    if not all_articles:
        print("⚠ No articles found. Exiting.")
        return

    # Save all data to a CSV file
    author_username = author_url.split('@')[-1].strip('/')
    csv_filename = f"{author_username}.csv"

    # Define CSV fieldnames
    fieldnames = [
        "Article_Title",
        "Article_Author",
        "Article_Source",
        "Article_Posted_Date",
        "Article_Link",
        "Article_Body",
        "Metadata"
    ]

    with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()  # Write CSV header
        for article in all_articles:
            article["Metadata"] = str(article.get("Metadata", {}))  # Convert metadata to string for CSV
            writer.writerow(article)

    print(f"✅ Scraping complete. Data saved to {csv_filename}")

# Example usage
if __name__ == "__main__":
    test_url = "https://substack.com/@cryptohayes"
    save_data(test_url)
