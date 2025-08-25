from django.urls import path
from . import views

# ...existing code...

urlpatterns = [
    # ...existing paths...
    path("mi/builder/", views.builder, name="mi_builder"),
    path("mi/builder/<int:datasource_id>/", views.builder, name="mi_builder_ds"),
    path(
        "mi/builder/<int:datasource_id>/viz/<int:viz_id>/",
        views.builder,
        name="mi_builder_viz",
    ),
    path(
        "mi/api/dataset/<int:datasource_id>/schema/",
        views.dataset_schema,
        name="mi_dataset_schema",
    ),
    path(
        "mi/api/viz/<int:viz_id>/", views.get_visualization, name="mi_get_visualization"
    ),
    path("mi/api/viz/save/", views.save_visualization, name="mi_save_visualization"),
    path(
        "mi/api/datasource/create/",
        views.create_datasource,
        name="mi_create_datasource",
    ),
]
