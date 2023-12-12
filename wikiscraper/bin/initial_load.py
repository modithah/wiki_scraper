# This is a sample Python script.
import dataclasses
import datetime
import json
import logging

from wikiscraper.scraper.data_mappings import Revision
from wikiscraper.scraper.wiki_api import get_all_revisions, get_users_info

PAGES_TO_DUMP = ["Lego Star Wars", "Lego", "Barbie"]
logger = logging.getLogger(__name__)


def save_all_revisions() -> None:
    logger.info("Retrieving revisions for all pages")
    for page_title in PAGES_TO_DUMP:
        dump_revision(page_title, datetime.datetime(2000, 1, 1))


def dump_revision(page_title: str, start_date: datetime.datetime) -> None:
    revisions = get_all_revisions(page_title, start_date)
    logging.info(f"Saving {len(revisions)} revisions for {page_title}")
    with open(f"data/{page_title}.json", "w", encoding="utf-8") as outfile:
        outfile.write(json.dumps([dataclasses.asdict(rev) for rev in revisions]))


def get_stored_revisions(page_title: str) -> list[Revision]:
    logger.info(f"Getting stored revisions for {page_title}")
    with open(f"data/{page_title}.json", "r", encoding="utf-8") as infile:
        return [Revision(**rev) for rev in json.loads(infile.read())]


def get_contributors_from_revisions(revisions: list[Revision]) -> list[dict]:
    logger.info(f"Calling the API to get contributors for {len(revisions)} revisions")
    contributor_ids = list({rev.user_id for rev in revisions if rev.user_id != 0})
    contributors = []
    chunk_size = 50
    for i in range(0, len(contributor_ids), chunk_size):
        chunk = contributor_ids[i : i + chunk_size]
        contributors.extend(get_users_info(chunk))
    return contributors


def save_contributors_file(contributors: list[dict], page: str) -> None:
    logger.info(f"Saving {len(contributors)} contributors for {page}")
    with open(f"data/{page}_contributors.json", "w", encoding="utf-8") as outfile:
        outfile.write(json.dumps(contributors))


def get_all_contributors_for_page(page_title: str) -> None:
    logger.info(f"Getting all contributors for {page_title}")
    revisions = get_stored_revisions(page_title)
    contributors = get_contributors_from_revisions(revisions)
    save_contributors_file(contributors, page_title)


def save_all_contributors() -> None:
    logger.info("Retrieving contributors for all pages")
    for page_title in PAGES_TO_DUMP:
        get_all_contributors_for_page(page_title)


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting initial load")
    save_all_revisions()
    save_all_contributors()
    logging.info("Initial load complete")
