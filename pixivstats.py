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
    def bookmark_view_ratio(self) -> float:
        return self.bookmark_count / self.view_count


class Follower(NamedTuple):
    id: int
    
    account_name: str
    nickname    : str


def list_artwork_metadata(user_id: int, session, content_type: str = '') -> list:
    """Fetch the metadata of the artworks posted by a specific user."""
    if content_type not in ('', 'illust', 'manga'):
        raise ValueError("`artwork_type` shall be 'illust', 'manga', or an empty string")
    
    # Fetch the artwork data on the first page
    page = session.user_illusts(user_id, type = content_type)
    artworks = [extract_artwork_metadata(work) for work in page.illusts]
    
    # Fetch the artwork data on the second and subsequent pages
    while True:
        next_query = session.parse_qs(page.next_url)
        if not next_query: break
        
        page = session.user_illusts(**next_query)
        artworks += [extract_artwork_metadata(work) for work in page.illusts]
    
    return artworks


def fetch_artwork_metadata(content_id: int, session) -> Artwork:
    artwork = session.illust_detail(content_id).illust
    return extract_artwork_metadata(artwork)


def list_followers(session) -> list:
    """Fetch the metadata of the users following the current user."""
    # Fetch the user data on the first page
    page = session.user_follower(session.user_id)
    followers = [extract_follower_metadata(preview) for preview in page.user_previews]
    
    # Fetch the user data on the second and subsequent pages
    while True:
        next_query = session.parse_qs(page.next_url)
        if not next_query: break
        
        page = session.user_follower(**next_query)
        followers += [extract_follower_metadata(preview) for preview in page.user_previews]
    
    return followers


def login(user_name: str, password: str):
    """Log-in to pixiv and return the session."""
    api = AppPixivAPI()
    api.login(user_name, password)
    
    return api


def extract_artwork_metadata(artwork_meta) -> Artwork:
    """Drop unnecessary artwork data and convert into a named tuple."""
    return Artwork(artwork_meta.id,
                   artwork_meta.user.id,
                   artwork_meta.title,
                   artwork_meta.user.name,
                   datetime.fromisoformat(artwork_meta.create_date),
                   artwork_meta.total_view,
                   artwork_meta.total_bookmarks)


def extract_follower_metadata(follower_preview) -> Follower:
    """Drop unnecessary follower data and convert into a named tuple."""
    return Follower(follower_preview.user.id,
                    follower_preview.user.account,
                    follower_preview.user.name)
