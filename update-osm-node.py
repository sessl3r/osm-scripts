#!/usr/bin/env python3

import argparse
import os
import json
import sys
from xml.etree import ElementTree

import osm

def parse_args():
    parser = argparse.ArgumentParser()
    osm.argparse_or_env(parser)
    parser.add_argument('node', type=str)
    parser.add_argument('--changeset', type=str, help="Changeset ID to be used")
    parser.add_argument('--mapillary', type=str, help="Add a mapillary id tag")
    parser.add_argument('--addname', action='store_true', help="Add missing name tag if not available")
    parser.add_argument('--delname', action='store_true', help="Delete name tag ")
    parser.add_argument('--addwikidata', action='store_true', help="Add missing species:wikidata tag if not available")
    parser.add_argument('--addbase', action='store_true', help="Add missing natural, leaf_type, leaf_cycle")
    parser.add_argument('--dryrun', action='store_true')
    parser.add_argument('--noask', action='store_true')
    return parser.parse_args()


def add_name_tag(et: ElementTree, fromtag: str):
    node = et.getroot()[0]
    for tag in node:
        if tag.attrib['k'] == 'name':
            return True # found so abort
    for tag in node:
        if tag.attrib['k'] == fromtag:
            osm.add_xml_tag(et, 'name', tag.attrib['v'])
            return True


def add_wikidata_tag(et: ElementTree):
    node = et.getroot()[0]
    for tag in node:
        if tag.attrib['k'] == 'species:wikidata':
            return False # found so abort
    for tag in node:
        if tag.attrib['k'] == 'species':
            if tag.attrib['v'] == 'Malus':
                osm.add_xml_tag(et, 'species:wikidata', 'Q104819')
            if tag.attrib['v'] == 'Pyrus':
                osm.add_xml_tag(et, 'species:wikidata', 'Q434')
            return True


def add_basedata_tags(et: ElementTree):
    osm.add_xml_tag(et, 'natural', 'tree', replace=True)
    osm.add_xml_tag(et, 'leaf_type', 'broadleaved', replace=True)
    osm.add_xml_tag(et, 'leaf_cycle', 'deciduous', replace=True)
    return True


def main(args: argparse.Namespace):
    api = osm.OSMApi(args.osmapi, args.osmtoken)
    response = api.get(f"node/{args.node}")
    if response.status_code != 200 or not response.text:
        print("Error in getting old node data, abort")
        return 1
    et = osm.et_fromstring(response.text)
    node = et.getroot()[0]
    modified = False

    if args.changeset:
        node.set('changeset', args.changeset)

    if args.mapillary:
        osm.add_xml_tag(et, 'mapillary', args.mapillary, replace=True)
        modified |= True

    if args.delname:
        for tag in node:
            if tag.attrib['k'] == 'name':
                node.remove(tag)
                modified = True
                break

    if args.addname:
        modified |= add_name_tag(et, 'taxon')

    if args.addwikidata:
        modified |= add_wikidata_tag(et)

    if args.addbase:
        modified |= add_basedata_tags(et)

    if not modified:
        print("No changes, not updating")
        return

    xmlstr = osm.et_tostring(et)
    if not args.noask:
        print(f"The following XML will be sent to OSM: {xmlstr}")
        q = input("\n\nProceed? (y/n)")
        if (q.lower() != 'y'):
            print("Aborting, bye")
            return
    
    print(f"Updating node {args.node} in changeset {args.changeset}")
    print(xmlstr)
    if not args.dryrun:
        response = api.put(f"node/{args.node}", data=xmlstr)
        if response.status_code != 200:
            print(response.text)


if __name__ == '__main__':
    main(parse_args())
