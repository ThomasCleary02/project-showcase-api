# yourapp/management/commands/scrape_medium.py

import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.dateparse import parse_date
from articles.models import Article

from typing import Optional

class MediumDateParser:
    @staticmethod
    def parse_medium_date(date_str: str) -> Optional[datetime.date]:
        """
        Parse Medium's date format (e.g., 'Feb 6') into a datetime.date object.
        Assumes current year if not specified.
        """
        if not date_str:
            return None
            
        try:
            # Remove any extra whitespace and split
            parts = date_str.strip().split()
            
            if len(parts) == 2:  # Format: "Feb 6"
                month, day = parts
                year = datetime.datetime.now().year
            elif len(parts) == 3:  # Format: "Feb 6, 2024"
                month, day, year = parts
                day = day.rstrip(',')
            else:
                return None
                
            # Convert to datetime
            date_str = f"{month} {day} {year}"
            return datetime.datetime.strptime(date_str, "%b %d %Y").date()
        except (ValueError, IndexError):
            return None

class Command(BaseCommand):
    help = 'Scrapes articles from a Medium profile and updates the database'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Medium username to scrape')
        parser.add_argument(
            '--replace',
            action='store_true',
            help='Replace all existing articles (default: only add new ones)',
        )

    def handle(self, *args, **options):
        username = options['username']
        replace = options['replace']
        
        self.stdout.write(f"Starting Medium scrape for user: {username}")
        
        try:
            # Initialize the scraper
            from articles.utils.scraper_util import MediumScraper  # Import your scraper class
            scraper = MediumScraper()
            
            # Fetch and parse the articles
            html_content = scraper.get_profile_page(username)
            articles = scraper.extract_article_details(html_content)
            
            with transaction.atomic():
                if replace:
                    self.stdout.write("Deleting existing articles...")
                    Article.objects.all().delete()
                
                created_count = 0
                updated_count = 0
                skipped_count = 0
                
                for article_data in articles:
                    # Parse the date
                    published_date = MediumDateParser.parse_medium_date(article_data.get('date'))
                    
                    # Prepare article data
                    article_dict = {
                        'title': article_data['title'],
                        'subtitle': article_data['subtitle'],
                        'url': article_data['link'],
                        'img_url': article_data['image_url'],
                        'published_date': published_date,
                    }
                    
                    try:
                        # Try to get existing article by URL
                        article, created = Article.objects.update_or_create(
                            url=article_dict['url'],
                            defaults=article_dict
                        )
                        
                        if created:
                            created_count += 1
                        else:
                            updated_count += 1
                            
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(
                            f"Error processing article '{article_dict['title']}': {str(e)}"
                        ))
                        skipped_count += 1
                
                # Print summary
                self.stdout.write(self.style.SUCCESS(
                    f"\nScraping completed:"
                    f"\n- Created: {created_count}"
                    f"\n- Updated: {updated_count}"
                    f"\n- Skipped: {skipped_count}"
                ))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Scraping failed: {str(e)}"))
            raise