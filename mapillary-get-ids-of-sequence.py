#!/usr/bin/env python3

import argparse
import os
import json
import requests


def parse_args():
    def env_or_required(key):
        return ({'default': os.environ.get(key)} if os.environ.get(key) else {'required': True} )

    parser = argparse.ArgumentParser()
    parser.add_argument('sequence')
    parser.add_argument('--mapillary', type=str, help="Mapillary token", **env_or_required('MAPILLARY_TOKEN'))
    return parser.parse_args()


def mapillary_get_sequence(id: str):
    url = f"https://graph.mapillary.com/image_ids?sequence_id={id}&access_token={os.environ.get('MAPILLARY_TOKEN')}"
    response = requests.get(url)
    return json.loads(response.text)['data']


def main(args: argparse.Namespace):
    for value in mapillary_get_sequence(args.sequence):
        print(value['id'])


if __name__ == '__main__':
    main(parse_args())
