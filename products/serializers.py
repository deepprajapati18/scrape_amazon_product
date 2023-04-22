from rest_framework import serializers
from utils.amazon_scraper import AmazonScrapper


class ScrapeProductsSerializers(serializers.Serializer):
    keyword = serializers.CharField()

    def create(self, validated_data):
        """Get data from Scrapper"""
        scrapper = AmazonScrapper(validated_data["keyword"])
        status, data = scrapper.do_process()
        if not status:
            raise serializers.ValidationError(data)
        return data
