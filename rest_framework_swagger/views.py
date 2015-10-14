import json

from django.views.generic import View
from django.utils.safestring import mark_safe
from django.shortcuts import render_to_response, RequestContext
from django.core.exceptions import PermissionDenied
from .config import SwaggerConfig

from rest_framework.views import Response, APIView
from rest_framework.settings import api_settings
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from rest_framework_swagger.urlparser import UrlParser
from rest_framework_swagger.docgenerator import DocumentationGenerator

import rest_framework_swagger as rfs


try:
    JSONRenderer = list(filter(
        lambda item: item.format == 'json',
        api_settings.DEFAULT_RENDERER_CLASSES,
    ))[0]
except IndexError:
    from rest_framework.renderers import JSONRenderer


class BaseSwaggerView(object):
    def check_permission(self, request, swagger_config_name):
        self.config = SwaggerConfig().get_config(swagger_config_name)
        if not self.has_permission(request):
            raise PermissionDenied()

    def has_permission(self, request):
        if self.config['is_superuser'] and not request.user.is_superuser:
            return False
        if self.config['is_authenticated'] and not request.user.is_authenticated():
            return False
        return True


class SwaggerUIView(BaseSwaggerView, View):
    def get(self, request, version, swagger_config_name=None):
        self.check_permission(request, swagger_config_name)

        data = {
            'swagger_settings': {
                'swagger_file': "%s/swagger.json" % self.get_full_base_path(request),
                'user_token': request.user.auth_token.key
            }
        }
        response = render_to_response(
            "rest_framework_swagger/index.html", RequestContext(request, data))

        return response

    def get_full_base_path(self, request):
        try:
            base_path = self.config['base_path']
        except KeyError:
            return request.build_absolute_uri(request.path).rstrip('/')
        else:
            protocol = 'https' if request.is_secure() else 'http'
            return '{0}://{1}'.format(protocol, base_path.rstrip('/'))


class Swagger2JSONView(BaseSwaggerView, APIView):
    renderer_classes = (JSONRenderer, )

    def get(self, request, version, swagger_config_name=None):
        self.check_permission(request, swagger_config_name)
        paths = self.get_paths()
        generator = DocumentationGenerator(for_user=request.user)
        return Response(generator.get_root(paths))

    def get_paths(self):
        urlparser = UrlParser()
        urlconf = getattr(self.request, "urlconf", None)
        exclude_namespaces = self.config.get('exclude_namespaces', [])
        exclude_module_paths = self.config.get('exclude_module_paths', [])
        include_module_paths = self.config.get('include_module_paths', [])
        exclude_url_patterns = self.config.get('exclude_url_patterns', [])

        return urlparser.get_apis(
            urlconf=urlconf,
            include_module_paths=include_module_paths,
            exclude_namespaces=exclude_namespaces,
            exclude_module_paths=exclude_module_paths,
            exclude_url_patterns=exclude_url_patterns)
