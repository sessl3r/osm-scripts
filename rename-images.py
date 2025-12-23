#!/usr/bin/env python3

import argparse
import logging
import os
import sys
import yaml


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', type=str, help="Folder to search for images")
    parser.add_argument('--data', default='data.yaml', help="All the Data")
    parser.add_argument('--offset', type=int, default=0, help="First image to use (offset)")
    parser.add_argument('--wiese', required=True, type=str, help="Wiesenname")
    parser.add_argument('--reihe', required=True, type=int, help="Reihennummer")
    parser.add_argument('--reverse', action="store_true", help="Reihe Rückwärts gelaufen")
    parser.add_argument('--doit', action="store_true", help="Rename the files")
    return parser.parse_args()


def main(args: argparse.Namespace):
    files = [f for f in sorted(os.listdir(args.folder)) if os.path.isfile(os.path.join(args.folder, f))]
    with open(args.data, "r") as f:
        data = yaml.safe_load(f)

    if args.wiese not in data:
        print(f"Wiese {args.wiese} not found in {args.data}, found: {list(data.keys())}")
        return 1
    wiese = data[args.wiese]

    if args.reihe not in wiese:
        print(f"Reihe {args.reihe} not found in {args.wiese}, found: {list(wiese.keys())}")
        return 1
    reihe = wiese[args.reihe]

    files = files[args.offset : args.offset + len(reihe)]
    if args.reverse:
        reihe = reihe[::-1]

    for idx in range(len(files)):
        file = files[idx]
        filedate = file.split('_')[1]
        name = reihe[idx].replace(' ', '-')
        newfile = f"{name}_{filedate}.jpg"
        print(f"{file} -> {newfile}")
        if args.doit:
            os.rename(os.path.join(args.folder, file), os.path.join(args.folder, newfile))


if __name__ == '__main__':
    main(parse_args())
