"""Write pixiv content metadata in CSV frormat."""

from datetime import date

from pixivstats import Artwork

_COLUMN_LABELS = ('fetched_on',
                  'content_id',
                  'author_id',
                  'posted_on',
                  'duration',
                  'view_count',
                  'bookmark_count',
                  'bookmark_view_ratio')

_HEADER_LINE = ",".join(_COLUMN_LABELS) + "\n"

DATE_FMT = '%Y/%m/%d'

def _write_csv_header(file, artwork: Artwork, comment: str = "# ,"):
    file.write(comment + f"author_name,{artwork.author_name},title,{artwork.title}\n")
    file.write(_HEADER_LINE)


def append_row(file_name, artwork: Artwork, date_ = None):
    today = date_ or date.today()
    
    with open(file_name, 'at', newline = '\r\n') as file:
        if file.tell() == 0: _write_csv_header(file, artwork)
        
        file.write(f"{today.strftime(DATE_FMT)},"
                   f"{artwork.content_id},"
                   f"{artwork.author_id},"
                   f"{artwork.posted_datetime.strftime(DATE_FMT)},"
                   f"{(today - artwork.posted_datetime.date()).days},"
                   f"{artwork.view_count},"
                   f"{artwork.bookmark_count},"
                   f"{artwork.bookmark_view_ratio}\n")
