# products/views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.retrieval_count += 1
        instance.retrieved_at = timezone.now()  # Update retrieval timestamp
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def top_retrieved(self, request):
        time_period = request.query_params.get('period', 'all')

        if time_period == 'day':
            time_threshold = timezone.now() - timedelta(days=1)
        elif time_period == 'week':
            time_threshold = timezone.now() - timedelta(weeks=1)
        else:
            time_threshold = None

        if time_threshold:
            products = Product.objects.filter(retrieved_at__gte=time_threshold).order_by('-retrieval_count')
        else:
            products = Product.objects.all().order_by('-retrieval_count')

        top_products = products[:5]
        serializer = self.get_serializer(top_products, many=True)
        return Response(serializer.data)
