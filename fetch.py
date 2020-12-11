#!/usr/bin/env python3

import json
from datetime import date

import statcsv
import followercsv
from pixivstats import *

def main():
    with open("config.json") as f: config = json.load(f)
    user_name = config['user_name']
    password  = config['password']
    targets   = config['target_content_ids']
    
    session = login(user_name, password)
    
    fetch_artwork_stats(targets, session)
    fetch_follower_list(session)


def fetch_artwork_stats(target_content_ids, session):
    for content_id in target_content_ids:
        file_name = f"{content_id:0d}.csv"
        
        work = fetch_artwork_metadata(content_id, session)
        statcsv.append_row(file_name, work)


def fetch_follower_list(session):
    followers = list_followers(session)
    
    today     = date.today()
    file_name = today.strftime('%Y%m%d') + "-follower.csv"
    
    followercsv.append_rows(file_name, followers)


if __name__ == '__main__': main()
