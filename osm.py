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


def add_xml_tag(et: ElementTree, key: str, value: str, replace = False):
    root = et.getroot()
    node = root[0]
    for tag in node:
        if key == tag.attrib['k']:
            if not replace:
                print(f"tag {key} already set to value {value}, use --force to overwrite")
                return
            tag.attrib['v'] = value
            return
    node.append(ElementTree.Element('tag', {'k':key,'v':value}))
    return et


def et_fromstring(data: str):
    return ElementTree.ElementTree(
            ElementTree.fromstring(data)
    )


def et_tostring(et: ElementTree):
    return ElementTree.tostring(et.getroot(), encoding='unicode')


def argparse_or_env(parser: argparse.ArgumentParser):
    """ Add needed OSM information either from environment or
        from arguments
    """
    def env_or_required(key):
        return ({'default': os.environ.get(key)} if os.environ.get(key) else {'required': True} )
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
    
    def post(self, endpoint: str, params = None, data = None):
        response = requests.post(f"{self.url}/{endpoint}",
                params = params,
                data = data,
                headers = {
                    "Authorization": f"Bearer {self.token}"
                }
        )
        return response
