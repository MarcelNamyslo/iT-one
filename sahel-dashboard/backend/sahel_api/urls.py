from django.urls import path
from .views import list_files, process_tiff, list_html_maps, save_map_data

urlpatterns = [
    path("files/", list_files, name="list_files"),
    path("process-tiff/<path:filepath>/", process_tiff, name="process_tiff"), 
    path("html-maps/", list_html_maps, name="list_html_maps"),
    path("save-map-data/", save_map_data, name="save_map_data"),
]
