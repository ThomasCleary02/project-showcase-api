# articles/management/commands/scrape.py

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.utils import OperationalError, ProgrammingError
from articles.models import Article  # Update this import to match your app name

class Command(BaseCommand):
    help = 'Scrapes articles from a Medium profile and updates the database'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Medium username to scrape')

    def handle(self, *args, **options):
        username = options['username']
        
        self.stdout.write(f"Starting Medium scrape for user: {username}")
        
        try:
            # Initialize the scraper
            from articles.utils.scraper_util import MediumScraper
            scraper = MediumScraper()
            
            # Fetch and parse the articles
            html_content = scraper.get_profile_page(username)
            articles = scraper.extract_article_details(html_content)
            
            created_count = 0
            updated_count = 0
            skipped_count = 0
            
            for article_data in articles:
                # Prepare base article data (required fields only)
                article_dict = {
                    'title': article_data['title'],
                    'subtitle': article_data['subtitle'] or '',
                    'url': article_data['link'],
                    'img_url': article_data['image_url'] or '',
                }
                
                try:
                    # First try to get the article
                    try:
                        article = Article.objects.get(url=article_dict['url'])
                        # Update existing article
                        for key, value in article_dict.items():
                            setattr(article, key, value)
                        article.save()
                        updated_count += 1
                        self.stdout.write(f"Updated: {article.title}")
                    except Article.DoesNotExist:
                        # Create new article
                        article = Article.objects.create(**article_dict)
                        created_count += 1
                        self.stdout.write(f"Created: {article.title}")
                            
                except Exception as e:
                    self.stdout.write(self.style.WARNING(
                        f"Error processing article '{article_dict['title']}': {str(e)}"
                    ))
                    skipped_count += 1
                    continue
            
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