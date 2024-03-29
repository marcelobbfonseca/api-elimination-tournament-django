"""
URL configuration for tournament_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
# from eliminationtournaments.views.views_wrappers import TournamentViewWrapper 
from eliminationtournaments.views.tournaments_views import TournamentViewSet
from eliminationtournaments.views.players_views import PlayerViewSet
from eliminationtournaments.views.positions_views import PositionViewSet, PositionAPIView
from eliminationtournaments.views.server_time_view import ServerTimeAPIView
from eliminationtournaments.views.index_views import IndexView

from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'tournaments', TournamentViewSet)
router.register(r'players', PlayerViewSet)
router.register(r'positions', PositionViewSet)


urlpatterns = [
    path('api/v2/', include(router.urls)),
    path('api/v2/positions/<int:id>/vote', view=PositionAPIView.as_view(), name='position-vote'),
    path('api/v2/time/', view=ServerTimeAPIView.as_view(), name='server-time'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    # path('', IndexView.as_view(), {'resource': ''}, name='index'),
    # re_path('^.*$', IndexView.as_view()),
    # path('<path:resource>', IndexView.as_view())
    # path('api/v1/tournament/', view=TournamentViewWrapper.as_view(), name='tournament-list'),
    # path('api/v1/tournament/<int:id>/', view=TournamentViewWrapper.as_view(), name='tournament-details'),
]
