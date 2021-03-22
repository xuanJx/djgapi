from rest_framework.routers import DefaultRouter

from bookapp import api_views

app_name = 'djgapi'

urlpatterns = [

]

router = DefaultRouter()
router.register('apibooks', api_views.BooksAPIView, basename='books')
router.register('apiauthors', api_views.AuthorAPIView, basename='authors')
router.register('apichapters', api_views.ChapterAPIView, basename='chapters')
router.register('apiuser', api_views.UserAPIView, basename='users')
router.register("apiscienceauthor", api_views.ScienceAuthorVPIView, basename='scienceauthor')
router.register('apisciencebooks', api_views.ScienceBooksVPIView, basename='sciencebooks')

urlpatterns += router.urls

