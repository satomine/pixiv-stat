#!/usr/bin/env python3

import argparse
import json
from datetime import date

import statcsv
import followercsv
from pixivstats import login, list_artwork_metadata, list_followers

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type', dest = 'content_type',
                        default = 'all', choices = ('all', 'i', 'illust', 'm', 'manga'),
                        help = "Target content type ('all' by default)")
    args = parser.parse_args()
    
    # Choose target content types
    if args.content_type == 'all'          : content_type = ''        # Both illustrations and manga
    if args.content_type in {'i', 'illust'}: content_type = 'illust'
    if args.content_type in {'m', 'manga'} : content_type = 'manga'
    
    with open("config.json") as f: config = json.load(f)
    user_name = config['user_name']
    password  = config['password']
    targets   = config['target_user_ids']
    
    session = login(user_name, password)
    
    for target_user_id in targets:
        artworks = list_artwork_metadata(target_user_id, session, content_type)
        write_artwork_stats(artworks)
    
    fetch_follower_list(session)


def write_artwork_stats(artworks):
    for artwork in artworks:
        file_name = f"{artwork.content_id:0d}.csv"
        statcsv.append_row(file_name, artwork)


def fetch_follower_list(session):
    followers = list_followers(session)
    
    today     = date.today()
    file_name = today.strftime('%Y%m%d') + "-follower.csv"
    
    followercsv.append_rows(file_name, followers)


if __name__ == '__main__': main()
