from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    # -----------------------------------
    # Hlavná stránka (životopis)
    # -----------------------------------
    path('', views.post_list, name='post_list'),

    # -----------------------------------
    # Blog / posty / životopis
    # -----------------------------------
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<int:pk>/remove/', views.post_remove, name='post_remove'),

    # -----------------------------------
    # Email / kontaktný formulár
    # -----------------------------------
    path('email/', views.send_email, name='send_email'),
    path('success/', views.success_view, name='success_view'),  
    path('unsuccess/', views.unsuccess_view, name='unsuccess_view'), 

    # -----------------------------------
    # Životopis
    # -----------------------------------
    path('zivo/', views.zivo_view, name='zivo_view'),
    path('en/zivo/', views.ang_zivo_view, name='zivo_en'),

    # -----------------------------------
    # Galéria / obrázky
    # -----------------------------------
    path('gallery/', views.gallery_view, name='gallery'),  
    path('image/<int:pk>/delete/', views.image_delete, name='image_delete'),

    # -----------------------------------
    # Reality / sledovanie cien
    # -----------------------------------
    path('reality/', views.home_view, name='home'),
    path('reality/delete/<int:pk>/', views.CenyDeleteView.as_view(), name='delete'),
    path('reality/update/', views.update_prices, name='update'),

    # -----------------------------------
    # Sql/testovanie
    # -----------------------------------
    path('sql-test/', views.sql_test_view, name='sql_test'),
    # HTML stránka s tlačidlom a spinnerom
    path("test_page/", views.run_tests_page, name="test_page"),
    # Endpoint pre JS, ktorý spúšťa testy a vracia JSON
    path("run_tests/", views.run_tests, name="run_tests_api"),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)