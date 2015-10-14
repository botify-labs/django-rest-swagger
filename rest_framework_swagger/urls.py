from django.conf.urls import patterns
from django.conf.urls import url
from rest_framework_swagger.views import SwaggerUIView, Swagger2JSONView

urlpatterns = patterns(
    '',
    url(
        r'^(?P<swagger_config_name>.+)/swagger\.json$',
        Swagger2JSONView.as_view(),
        name='django.swagger.2.0.json.view'
    ),
    url(
        r'^swagger\.json$',
        Swagger2JSONView.as_view(),
        name='django.swagger.2.0.json.view'
    ),
    url(
        r'^(?P<swagger_config_name>.+)/?$',
        SwaggerUIView.as_view(),
        name="django.swagger.base.view"
    ),
    url(
        r'^$',
        SwaggerUIView.as_view(),
        name="django.swagger.base.view"
    )
)
