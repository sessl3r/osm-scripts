#!/usr/bin/env python3

import argparse
import os
import sys
from xml.etree import ElementTree

import osm


def parse_args():
    parser = argparse.ArgumentParser()
    osm.argparse_or_env(parser)
    parser.add_argument('--comment', type=str)
    parser.add_argument('--close', type=str)
    return parser.parse_args()


def main(args: argparse.Namespace):
    api = osm.OSMApi(args.osmapi, args.osmtoken)
    et = osm.base_xml()
    xmlosm = et.getroot()
    changset = ElementTree.SubElement(xmlosm, 'changeset')

    if args.close:
        response = api.put(f"changeset/{args.close}/close")
        print(response.text)
        return

    if args.comment:
        tag = ElementTree.SubElement(changset, 'tag')
        tag.set('k', 'comment')
        tag.set('v', args.comment)

    xmlstr = osm.et_tostring(et)
    response = api.put("changeset/create",
            data = ElementTree.tostring(xmlosm, encoding='utf-8'),
    )
    print(response.text)


if __name__ == '__main__':
    main(parse_args())
