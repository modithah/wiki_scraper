import json
import logging

from wikiscraper.data_access.data_mappings import Revision, factory

logger = logging.getLogger(__name__)


def get_stored_revisions(page_title: str) -> list[Revision]:
    logger.info(f"Getting stored revisions for {page_title}")
    with open(f"data/{page_title}.json", "r", encoding="utf-8") as infile:
        return [factory.load(rev, Revision) for rev in json.loads(infile.read())]


def get_stored_contributors(page_title: str) -> list[dict]:
    logger.info(f"Getting stored contributors for {page_title}")
    with open(f"data/{page_title}_contributors.json", "r", encoding="utf-8") as infile:
        return json.loads(infile.read())
