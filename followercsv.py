"""List pixiv followers in CSV frormat."""

from pixivstats import Follower

_COLUMN_LABELS = ('id', 'account_name', 'author_id')
_HEADER_LINE   = ",".join(_COLUMN_LABELS) + "\n"

def _write_csv_header(file): file.write(_HEADER_LINE)


def append_row(file_path, follower: Follower):
    with open(file_path, 'at', newline = '\r\n') as file:
        if file.tell() == 0: _write_csv_header(file)
        
        file.write(f"{follower.id},"
                   f"{follower.account_name},"
                   f"{follower.nickname}\n")


def append_rows(file_path, followers):
    for follower in followers: append_row(file_path, follower)
