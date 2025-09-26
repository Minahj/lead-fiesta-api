"""
Management command to test the scrapers functionality.
"""
import json
from django.core.management.base import BaseCommand
from scrapers.services import InstagramScraperService, TikTokScraperService


class Command(BaseCommand):
    help = 'Test the Instagram and TikTok scrapers'

    def add_arguments(self, parser):
        parser.add_argument(
            '--instagram',
            type=str,
            help='Instagram profile URL or username to test'
        )
        parser.add_argument(
            '--tiktok',
            type=str,
            help='TikTok profile URL or username to test'
        )

    def handle(self, *args, **options):
        if options['instagram']:
            self.test_instagram(options['instagram'])
        
        if options['tiktok']:
            self.test_tiktok(options['tiktok'])
        
        if not options['instagram'] and not options['tiktok']:
            self.stdout.write(
                self.style.WARNING(
                    'Please provide --instagram or --tiktok argument'
                )
            )

    def test_instagram(self, url):
        self.stdout.write(f'Testing Instagram scraper with: {url}')
        try:
            scraper = InstagramScraperService()
            result = scraper.scrape_profile(url)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Instagram scraping successful:\n{json.dumps(result, indent=2)}'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Instagram scraping failed: {e}')
            )

    def test_tiktok(self, url):
        self.stdout.write(f'Testing TikTok scraper with: {url}')
        try:
            scraper = TikTokScraperService()
            result = scraper.scrape_profile(url)
            self.stdout.write(
                self.style.SUCCESS(
                    f'TikTok scraping successful:\n{json.dumps(result, indent=2)}'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'TikTok scraping failed: {e}')
            )
