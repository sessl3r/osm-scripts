import argparse
import os
import sys
import requests
from xml.etree import ElementTree


def base_xml():
    osm = ElementTree.Element('osm')
    et = ElementTree.ElementTree(osm)
    osm.set('version', '0.6')
    osm.set('generator', 'python')
    return et


def argparse_or_env(parser: argparse.ArgumentParser):
    """ Add needed OSM information either from environment or
        from arguments
    """
    def env_or_required(key):
        return (
            {'default': os.environ.get(key)} if os.environ.get(key)
            else {'required': True}
        )
    parser.add_argument('--osmapi', **env_or_required('OSM_API'))
    parser.add_argument('--osmtoken', **env_or_required('OSM_TOKEN'))

class OSMApi():
    def __init__(self, url, token):
        self.url = url
        self.token = token

    def get(self, endpoint: str, params = None):
        response = requests.get(f"{self.url}/{endpoint}",
                headers = {
                    "Authorization": f"Bearer {self.token}"
                }
        )
        return response
    
    def put(self, endpoint: str, params = None, data = None):
        response = requests.put(f"{self.url}/{endpoint}",
                data = data,
                headers = {
                    "Authorization": f"Bearer {self.token}"
                }
        )
        return response
    
    def post(self, endpoint: str, params = None):
        response = requests.post(f"{self.url}/{endpoint}",
                data = data,
                headers = {
                    "Authorization": f"Bearer {self.token}"
                }
        )
        return response
