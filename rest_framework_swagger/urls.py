from django.conf.urls import patterns
from django.conf.urls import url
from rest_framework_swagger.views import (SwaggerResourcesView, SwaggerApiView, SwaggerUIView,
                                          Swagger2JSONView)

urlpatterns = patterns(
    '',
    url(r'^$', SwaggerUIView.as_view(), name="django.swagger.base.view"),
    url(r'^api-docs/$', SwaggerResourcesView.as_view(), name="django.swagger.resources.view"),
    url(r'^swagger\.json$', Swagger2JSONView.as_view(), name='django.swagger.2.0.json.view'),
)
