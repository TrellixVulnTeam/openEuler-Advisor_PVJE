#!/usr/bin/python3
"""
Blueprint collection trying to page
"""
from packageship.application.apps.package import package, api as package_api

blue_point = [
    (package, package_api)
]

__all__ = ['blue_point']