from rest_framework import viewsets
from .models import Article
from .serializers import ArticleSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()