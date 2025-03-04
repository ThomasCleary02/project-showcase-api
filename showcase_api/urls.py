"""
URL configuration for project_showcase project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from projects.views import ProjectViewSet
from articles.views import ArticleViewSet

# Projects Router
projects_router = routers.SimpleRouter()
projects_router.register(
    r'projects',
    ProjectViewSet,
    basename='project',
)

# Article Router
articles_router = routers.SimpleRouter()
articles_router.register(
    r'articles',
    ArticleViewSet,
    basename='article',
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(projects_router.urls)),
    path('api/', include(articles_router.urls))
]
