# This is a sample Python script.
import datetime
import logging


from wikiscraper.data_access.data_reader import get_stored_revisions
from wikiscraper.data_access.data_writer import store_revisions, store_contributors
from wikiscraper.scraper.wiki_api import get_all_revisions, get_users_info
from wikiscraper.data_access.data_mappings import Revision

PAGES_TO_DUMP = ["Lego Star Wars", "Lego", "Barbie"]
logger = logging.getLogger(__name__)


def save_all_revisions() -> None:
    logger.info("Retrieving revisions for all pages")
    for page_title in PAGES_TO_DUMP:
        save_revisions(page_title, datetime.datetime(2000, 1, 1))


def save_revisions(page_title: str, start_date: datetime.datetime) -> None:
    revisions = get_all_revisions(page_title, start_date)
    store_revisions(page_title, revisions)


def get_contributors_from_revisions(revisions: list[Revision]) -> list[dict]:
    logger.info(f"Calling the API to get contributors for {len(revisions)} revisions")
    contributor_ids = list({rev.user_id for rev in revisions if rev.user_id != 0})
    contributors = []
    chunk_size = 50
    for i in range(0, len(contributor_ids), chunk_size):
        chunk = contributor_ids[i : i + chunk_size]
        contributors.extend(get_users_info(chunk))
    return contributors


def get_all_contributors_for_page(page_title: str) -> None:
    logger.info(f"Getting all contributors for {page_title}")
    revisions = get_stored_revisions(page_title)
    contributors = get_contributors_from_revisions(revisions)
    store_contributors(contributors, page_title)


def save_all_contributors() -> None:
    logger.info("Retrieving contributors for all pages")
    for page_title in PAGES_TO_DUMP:
        get_all_contributors_for_page(page_title)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting initial load")
    save_all_revisions()
    save_all_contributors()
    logging.info("Initial load complete")
