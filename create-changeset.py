#!/usr/bin/env python3

import argparse
import os
import sys
import requests
from xml.etree import ElementTree

import osm


def parse_args():
    parser = argparse.ArgumentParser()
    osm.argparse_or_env(parser)
    parser.add_argument('--comment', type=str)
    return parser.parse_args()

def add_tag(xml: str, key: str, value: str, force = False):
    et = ElementTree.fromstring(xml)
    if len(et) != 1:
        raise ExecutionError("ERROR: invalid xml received from OSM, aborting")
    node = et[0]
    for tag in node:
        if key == tag.attrib['k'] and not force:
            print(f"tag {key} already set to value {value}, use --force to overwrite")
            return
    node.append(ElementTree.Element('tag', {'k':key,'v':value}))

    return ElementTree.tostring(et, encoding='utf-8')

def main(args: argparse.Namespace):
    api = osm.OSMApi(args.osmapi, args.osmtoken)
    et = osm.base_xml()
    xmlosm = et.getroot()
    changset = ElementTree.SubElement(xmlosm, 'changeset')

    if args.comment:
        tag = ElementTree.SubElement(changset, 'tag')
        tag.set('k', 'comment')
        tag.set('v', args.comment)

    print("The following XML will be sent to OSM:")
    et.write(sys.stdout.buffer, encoding='utf-8', xml_declaration=True)
    q = input("\n\nProceed? (y/n)")
    if (q.lower() != 'y'):
        print("Aborting, bye")

    response = api.put("changeset/create",
            data = ElementTree.tostring(xmlosm, encoding='utf-8'),
    )
    print(response.text)


if __name__ == '__main__':
    main(parse_args())
