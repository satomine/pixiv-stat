from typing   import NamedTuple
from datetime import datetime

from pixivpy3 import AppPixivAPI

class Artwork(NamedTuple):
    content_id : int
    author_id  : int
    title      : str
    author_name: str
    
    posted_datetime: datetime
    
    view_count    : int
    bookmark_count: int
    
    @property
    def bookmark_view_ratio(self):
        return self.bookmark_count / self.view_count


class Follower(NamedTuple):
    id: int
    
    account_name: str
    nickname    : str


def list_artwork_metadata(user_id: int, session):
    """Fetch the metadata of the works posted by a specific user."""
    page = session.user_illusts(user_id, type  = "")
    artworks = [extract_artwork_metadata(work) for work in page.illusts]
    
    while True:
        next_query = session.parse_qs(page.next_url)
        if not next_query: break
        
        page = session.user_illusts(**next_query)
        artworks += [extract_artwork_metadata(work) for work in page.illusts]
    
    return artworks


def fetch_artwork_metadata(content_id: int, session):
    artwork = session.illust_detail(content_id).illust
    return extract_artwork_metadata(artwork)


def list_followers(session):
    page = session.user_follower(session.user_id)
    followers = [extract_follower_metadata(preview) for preview in page.user_previews]
    
    while True:
        next_query = session.parse_qs(page.next_url)
        if not next_query: break
        
        page = session.user_follower(**next_query)
        followers += [extract_follower_metadata(preview) for preview in page.user_previews]
    
    return followers


def login(user_name: str, password: str):
    """Log-in to pixiv and return the session"""
    api = AppPixivAPI()
    api.login(user_name, password)
    
    return api


def extract_artwork_metadata(artwork_meta):
    """Drop unnecessary artwork data and convert into a named tuple."""
    return Artwork(artwork_meta.id,
                   artwork_meta.user.id,
                   artwork_meta.title,
                   artwork_meta.user.name,
                   datetime.fromisoformat(artwork_meta.create_date),
                   artwork_meta.total_view,
                   artwork_meta.total_bookmarks)


def extract_follower_metadata(follower_preview):
    """Drop unnecessary follower data and convert into a named tuple."""
    return Follower(follower_preview.user.id,
                    follower_preview.user.account,
                    follower_preview.user.name)
