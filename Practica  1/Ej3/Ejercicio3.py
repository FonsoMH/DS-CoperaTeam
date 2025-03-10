import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import yaml
from abc import ABC, abstractmethod


# Strategy Interface
class ScraperStrategy(ABC):
    @abstractmethod
    def scrape(self, url):
        pass

# Concrete Strategy: BeautifulSoup
class BeautifulSoupScraper(ScraperStrategy):
    def scrape(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return self.extract_quotes(soup)
    
    def extract_quotes(self, soup):
        quotes_data = []
        quotes = soup.find_all('div', class_='quote')
        for quote in quotes:
            text = quote.find('span', class_='text').get_text()
            author = quote.find('small', class_='author').get_text()
            tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]
            quotes_data.append({'quote': text, 'author': author, 'tags': tags})
        return quotes_data

# Concrete Strategy: Selenium
class SeleniumScraper(ScraperStrategy):
    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(service=Service(), options=options)
    
    def scrape(self, url):
        self.driver.get(url)
        quotes_data = self.extract_quotes()
        return quotes_data
    
    def extract_quotes(self):
        quotes_data = []
        quotes = self.driver.find_elements(By.CLASS_NAME, 'quote')
        for quote in quotes:
            text = quote.find_element(By.CLASS_NAME, 'text').text
            author = quote.find_element(By.CLASS_NAME, 'author').text
            tags = [tag.text for tag in quote.find_elements(By.CLASS_NAME, 'tag')]
            quotes_data.append({'quote': text, 'author': author, 'tags': tags})
        return quotes_data
    
    def close(self):
        self.driver.quit()

# Context Class
class ScraperContext:
    def __init__(self, strategy: ScraperStrategy):
        self.strategy = strategy
    
    def set_strategy(self, strategy: ScraperStrategy):
        self.strategy = strategy
    
    def scrape_pages(self, base_url, pages=5):
        all_quotes = []
        for page in range(1, pages + 1):
            url = f"{base_url}/page/{page}/"
            print(f"Scraping {url}")
            all_quotes.extend(self.strategy.scrape(url))
        return all_quotes

# Save to YAML
def save_to_yaml(data, filename='quotes.yaml'):
    with open(filename, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, allow_unicode=True, default_flow_style=False)

# Main Execution
if __name__ == '__main__':
    base_url = 'https://quotes.toscrape.com'
    
    # Using BeautifulSoup
    print("Using BeautifulSoup...")
    context = ScraperContext(BeautifulSoupScraper())
    quotes_bs = context.scrape_pages(base_url)
    save_to_yaml(quotes_bs, 'quotes_bs.yaml')
    
    # Using Selenium
    print("Using Selenium...")
    selenium_scraper = SeleniumScraper()
    context.set_strategy(selenium_scraper)
    quotes_selenium = context.scrape_pages(base_url)
    selenium_scraper.close()
    save_to_yaml(quotes_selenium, 'quotes_selenium.yaml')
    
    print("Scraping completed. Data saved to YAML files.")
