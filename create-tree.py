#!/usr/bin/env python3

import argparse
import os
import exifread
import sys
from xml.etree import ElementTree

import osm


def parse_args():
    parser = argparse.ArgumentParser()
    osm.argparse_or_env(parser)
    parser.add_argument('--changeset', type=str, help="changeset id to add element to")
    parser.add_argument('--image', type=str, required=True, help="Image for GPS extraction")
    parser.add_argument('--species', type=str, choices=['Apfel', 'Birne', 'Pflaume'])
    parser.add_argument('--name', type=str)
    parser.add_argument('--startdate', type=str)
    parser.add_argument('--dryrun', action='store_true')
    parser.add_argument('--noask', action='store_true')
    return parser.parse_args()


def main(args: argparse.Namespace):
    api = osm.OSMApi(args.osmapi, args.osmtoken)
    et = osm.base_xml()
    xmlosm = et.getroot()
    node = ElementTree.SubElement(xmlosm, 'node')

    if args.changeset:
        node.set('changeset', args.changeset)

    if args.image:
        with open(args.image, "rb") as f:
            exiftags = exifread.process_file(f, builtin_types=True)
        lat, lon = exifread.utils.get_gps_coords(exiftags)
        node.set('lat', str(lat))
        node.set('lon', str(lon))

    osm.add_xml_tag(et, 'natural', 'tree')
    osm.add_xml_tag(et, 'leaf_type', 'broadleaved')
    osm.add_xml_tag(et, 'leaf_cycle', 'deciduous')

    if args.species:
        osm.add_xml_tag(et, 'species:de', args.species)
        if args.species == 'Apfel':
            osm.add_xml_tag(et, 'species', "Malus")
            osm.add_xml_tag(et, 'species:wikidata', "Q104819")
        elif args.species == 'Birne':
            osm.add_xml_tag(et, 'species', "Pyrus")
            osm.add_xml_tag(et, 'species:wikidata', "Q434")
        elif args.species == 'Pflaume':
            osm.add_xml_tag(et, 'species', "Prunus domestica")
            osm.add_xml_tag(et, 'species:wikidata', "Q44120")

    if args.name:
        osm.add_xml_tag(et, 'taxon', args.name)

    if args.startdate:
        osm.add_xml_tag(et, 'start_date', args.startdate)

    xmlstr = osm.et_tostring(et)
    print(f"The following XML will be sent to OSM: {xmlstr}")
    if not args.noask:
        q = input("\n\nProceed? (y/n)")
        if (q.lower() != 'y'):
            print("Aborting, bye")
            return

    if not args.dryrun and args.changeset:
        response = api.post("nodes", data = xmlstr)
        print(response.text)


if __name__ == '__main__':
    main(parse_args())
