from crawl4ai import BrowserConfig, CrawlerRunConfig, CacheMode, AsyncWebCrawler
from bs4 import BeautifulSoup
import csv
import re
import requests

class CrawlerAndScraperMeta(type):
    """
    Metaclass that ensures only one instance of CrawlerAndScraper is created (Singleton pattern).
    """
    __instances = {}

    def __call__(self, *args, **kwds):
        if self not in self.__instances:
            self.__instances[self] = super().__call__(*args, **kwds)
        else:
            print("Error! Class instance already exists.")
        return self.__instances[self]

class CrawlerAndScraper(metaclass=CrawlerAndScraperMeta):
    """
    A class to handle web crawling and scraping tasks, specifically for arXiv papers.
    Includes methods for asynchronous crawling, parsing, and saving scraped data.
    """

    async def crawler(self):
        """
        Performs asynchronous web crawling to fetch data from a specified URL using `crawl4ai`.
        
        Returns:
            str: The crawled HTML content, formatted as either fit HTML or markdown.
        """
        browser_cfg = BrowserConfig(
            browser_type="chromium", headless=True, verbose=True
        )

        run_cfg = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,  # Bypass caching to always fetch fresh content
            css_selector="*",  # Selects all elements in the HTML
            word_count_threshold=10,  # Minimum word count for an element to be considered
            screenshot=True,  # Takes a screenshot of the page
        )

        async with AsyncWebCrawler(config=browser_cfg) as crawler:
            result = await crawler.arun(
                url="https://arxiv.org/list/cs.AI/recent", config=run_cfg
            )

            # Print previews of different formats of extracted content
            print("Markdown Content:\n", result.markdown[:500])
            print(
                "Fit HTML Content:\n",
                result.fit_html[:500] if result.fit_html else "None",
            )
            print(
                "Full HTML Content:\n",
                result.full_html[:500] if hasattr(result, "full_html") else "None",
            )

            # Save the markdown content to a file
            if result.markdown:
                with open("result-markdown.txt", "w") as file:
                    file.write(result.markdown)

            return result.fit_html or result.markdown

    def scraper(self, crawler_result):
        """
        Parses the result from the crawler and extracts data about papers,
        saving it to a CSV file.

        Args:
            crawler_result (str): The HTML or markdown content retrieved by the crawler.

        Returns:
            list: A list of dictionaries containing parsed paper data.
        """
        data = []
        entries = re.findall(r".*\n.*\n.*(?<=Title)", crawler_result, re.DOTALL)

        for entry in entries:
            arxiv_id, paper_link, title, authors_block, pages = entry

            # Extract author names from square brackets
            authors = re.findall(r"\[([^\]]+)\]", authors_block)
            authors_list = ", ".join(authors) if authors else "Unknown"

            # Append the extracted data to the list
            data.append(
                {
                    "title": title.strip() if title.strip() else "Unknown Title",
                    "authors": authors_list,
                    "link": paper_link.strip(),
                    "pages": pages.strip() if pages.strip() else "Unknown Pages",
                }
            )

        # Save the extracted data to a CSV file
        if data:
            output_file = "/app/data/arxiv_papers.csv"
            with open(output_file, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(
                    file, fieldnames=["title", "authors", "link", "pages"]
                )
                writer.writeheader()
                writer.writerows(data)

            print(f"Data successfully saved to {output_file}.")
        else:
            print("No valid data found to save. Check the markdown structure or regex.")

        return data

    def scrape_arxiv(self):
        """
        Performs web scraping of the arXiv computer science AI papers page using BeautifulSoup.
        Extracts details like title, authors, link, and pages, and saves the data to a CSV file.
        """
        url = "https://arxiv.org/list/cs.AI/recent"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch page: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, "html.parser")

        papers = []
        for dt, dd in zip(soup.find_all("dt"), soup.find_all("dd")):
            link_tag = dt.find("a", title="Abstract")
            paper_link = (
                f"https://arxiv.org{link_tag['href']}" if link_tag else "Unknown"
            )

            # Extract and clean the title
            title = dd.find("div", class_="list-title mathjax")
            title = title.text.replace("Title:", "").strip() if title else "Unknown"

            # Extract author names
            authors = dd.find("div", class_="list-authors")
            author_list = (
                ", ".join(a.text.strip() for a in authors.find_all("a"))
                if authors
                else "Unknown"
            )

            # Extract page information if available
            comments = dd.find("div", class_="list-comments")
            pages = "Unknown"
            if comments and "pages" in comments.text:
                pages = comments.text.split("pages")[0].split()[-1] + " pages"

            # Append extracted paper details
            papers.append(
                {
                    "title": title,
                    "authors": author_list,
                    "link": paper_link,
                    "pages": pages,
                }
            )

        # Save data to CSV file
        if papers:
            output_file = "/app/data/arxiv_papers.csv"
            with open(output_file, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(
                    file, fieldnames=["title", "authors", "link", "pages"]
                )
                writer.writeheader()
                writer.writerows(papers)
            print(f"Data successfully saved to {output_file}.")
        else:
            print("No data found on the page.")

    def main(self):
        """
        Orchestrates the crawling and scraping processes.
        Currently calls the `scrape_arxiv` method for static scraping.
        """
        self.scrape_arxiv()

if __name__ == "__main__":
    crawler_scraper_control = CrawlerAndScraper()
    crawler_scraper_control.main()
