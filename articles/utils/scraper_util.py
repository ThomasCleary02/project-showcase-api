# articles/management/commands/scrape_medium.py

import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.utils import OperationalError, ProgrammingError
from articles.models import Article

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
                    # Prepare base article data (required fields only)
                    article_dict = {
                        'title': article_data['title'],
                        'subtitle': article_data['subtitle'],
                        'url': article_data['link'],
                        'img_url': article_data['image_url'],
                    }
                    
                    try:
                        # Try to get existing article by URL
                        article, created = Article.objects.get_or_create(
                            url=article_dict['url'],
                            defaults=article_dict
                        )
                        
                        # Update existing article if needed
                        if not created:
                            for key, value in article_dict.items():
                                setattr(article, key, value)
                            article.save()
                        
                        if created:
                            created_count += 1
                            self.stdout.write(f"Created: {article.title}")
                        else:
                            updated_count += 1
                            self.stdout.write(f"Updated: {article.title}")
                            
                    except (OperationalError, ProgrammingError) as e:
                        if 'published_date' in str(e):
                            # Remove published_date and try again
                            if 'published_date' in article_dict:
                                del article_dict['published_date']
                            article, created = Article.objects.get_or_create(
                                url=article_dict['url'],
                                defaults=article_dict
                            )
                            if created:
                                created_count += 1
                            else:
                                updated_count += 1
                        else:
                            self.stdout.write(self.style.WARNING(
                                f"Error processing article '{article_dict['title']}': {str(e)}"
                            ))
                            skipped_count += 1
                            continue
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