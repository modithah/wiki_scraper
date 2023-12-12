# This is a sample Python script.
import dataclasses
import datetime
import json

from wikiscraper.scraper.data_mappings import Revision
from wikiscraper.scraper.wiki_api import get_all_revisions, get_users_info

PAGES_TO_DUMP = ["Lego Star Wars", "Lego", "Barbie"]


def dump_all_revisions() -> None:
    for page_title in PAGES_TO_DUMP:
        dump_revision(page_title, datetime.datetime(2000, 1, 1))


def dump_revision(page_title: str, start_date: datetime) -> None:
    revisions = get_all_revisions(page_title, start_date)
    with open(f"data/{page_title}.json", "w") as outfile:
        outfile.write(json.dumps([dataclasses.asdict(rev) for rev in revisions]))


def get_stored_revisions(page_title: str) -> list[Revision]:
    with open(f"data/{page_title}.json", "r") as infile:
        return [Revision(**rev) for rev in json.loads(infile.read())]


def get_contributors_from_revisions(revisions: list[Revision]) -> list[dict]:
    contributor_ids = list(set([rev.user_id for rev in revisions if rev.user_id != 0]))
    contributors = []
    chunk_size = 50
    for i in range(0, len(contributor_ids), chunk_size):
        chunk = contributor_ids[i:i + chunk_size]
        contributors.extend(get_users_info(chunk))
    return contributors


def save_contributors_file(contributors: list[dict], page: str) -> None:
    with open(f"data/{page}_contributors.json", "w") as outfile:
        outfile.write(json.dumps(contributors))


def get_all_contributors_for_page(page_title: str) -> None:
    revisions = get_stored_revisions(page_title)
    contributors = get_contributors_from_revisions(revisions)
    save_contributors_file(contributors, page_title)

def dump_all_contributors() -> None:
    for page_title in PAGES_TO_DUMP:
        get_all_contributors_for_page(page_title)


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    # dump_revision("Lego Star Wars", datetime.datetime(2023, 1, 1))
    # get_conributors("Lego")
    # print(get_stored_revisions("Lego Star Wars"))
    # for x in get_stored_revisions("Lego Star Wars"):
    #     print(x)
    # get_all_contributors_for_page("Lego")
    dump_all_contributors()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
