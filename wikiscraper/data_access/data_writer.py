import json
import logging

from wikiscraper.data_access.data_mappings import Revision, factory

logger = logging.getLogger(__name__)


def store_revisions(page_title: str, revisions: list[Revision]) -> None:
    logging.info(f"Saving {len(revisions)} revisions for {page_title}")
    with open(f"data/{page_title}.json", "w", encoding="utf-8") as outfile:
        outfile.write(json.dumps([factory.dump(rev) for rev in revisions]))


def store_contributors(contributors: list[dict], page: str) -> None:
    logger.info(f"Saving {len(contributors)} contributors for {page}")
    with open(f"data/{page}_contributors.json", "w", encoding="utf-8") as outfile:
        outfile.write(json.dumps(contributors))
