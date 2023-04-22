from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from products.serializers import ScrapeProductsSerializers


# /scrape-products/
class ScrapeProductsView(GenericAPIView):
    serializer_class = ScrapeProductsSerializers

    def post(self, request, *args, **kwargs):
        """Post method to scrape products"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data, status=status.HTTP_200_OK)
