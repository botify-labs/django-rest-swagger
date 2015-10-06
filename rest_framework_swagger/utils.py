# -*- coding: utf-8 -*-


def extract_base_path(path):
    """
    extracts the base_path (defined on settings) at the begining of the path
    e.g:
        SWAGGER_SETTINGS["basePath"] = "/foo"
        extract_base_path(path="/foo/bar") => "/bar"
    """
    from rest_framework_swagger import SWAGGER_SETTINGS
    base_path = SWAGGER_SETTINGS.get("basePath", '')
    if path.startswith(base_path):
        path = path[len(base_path):]
    return path
