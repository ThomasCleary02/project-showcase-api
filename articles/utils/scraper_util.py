import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from urllib.parse import urljoin
import json

class MediumScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
    def get_profile_page(self, username: str) -> str:
        """
        Fetch the Medium profile page content.
        
        Args:
            username (str): Medium username (without @)
            
        Returns:
            str: HTML content of the profile page
        """
        if username.startswith('@'):
            username = username[1:]
            
        url = f'https://medium.com/@{username}'
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch profile page: {str(e)}")

    def extract_article_details(self, html_content: str) -> List[Dict[str, str]]:
        """
        Extract article details from Medium profile page HTML content.
        
        Args:
            html_content (str): HTML content to parse
            
        Returns:
            List[Dict[str, str]]: List of dictionaries containing article details
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = soup.find_all('article')
        results = []
        
        for article in articles:
            article_data = {
                'title': '',
                'subtitle': '',
                'link': '',
                'image_url': '',
                'date': ''
            }
            
            # Extract title
            title_element = article.find('h2')
            if title_element:
                article_data['title'] = title_element.get_text(strip=True)
            
            # Extract subtitle
            subtitle_element = article.find('h3')
            if subtitle_element:
                article_data['subtitle'] = subtitle_element.get_text(strip=True)
            
            # Extract link
            link_element = article.find('a', href=True)
            if link_element:
                article_data['link'] = urljoin('https://medium.com', link_element['href'])
            
            # Extract image URL
            image_element = article.find('img', {'alt': article_data['title']})
            if image_element and 'src' in image_element.attrs:
                article_data['image_url'] = image_element['src']
            
            # Extract date
            date_element = article.find('span', string=lambda text: text and any(month in text for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']))
            if date_element:
                article_data['date'] = date_element.get_text(strip=True)
            
            if article_data['title']:  # Only add articles that have at least a title
                results.append(article_data)
        
        return results

    def save_to_json(self, articles: List[Dict[str, str]], filename: str):
        """
        Save the extracted articles to a JSON file.
        
        Args:
            articles (List[Dict[str, str]]): List of article dictionaries
            filename (str): Output filename
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(articles, f, indent=2, ensure_ascii=False)

def main():
    # Initialize scraper
    scraper = MediumScraper()
    
    try:
        # Get username from command line or use default
        username = "@thomcleary15"
        
        # Fetch and parse the profile page
        print(f"Fetching articles for {username}...")
        html_content = scraper.get_profile_page(username)
        
        # Extract article details
        articles = scraper.extract_article_details(html_content)
        
        # Save to JSON file
        output_filename = f"medium_{username.replace('@', '')}_articles.json"
        scraper.save_to_json(articles, output_filename)
        
        # Print results
        print(f"\nFound {len(articles)} articles:")
        for idx, article in enumerate(articles, 1):
            print(f"\nArticle {idx}:")
            for key, value in article.items():
                print(f"{key}: {value}")
                
        print(f"\nResults have been saved to {output_filename}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()