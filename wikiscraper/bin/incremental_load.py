import datetime

from wikiscraper.bin.initial_load import get_contributors_from_revisions
from wikiscraper.data_access.data_mappings import Revision
from wikiscraper.data_access.data_reader import get_stored_revisions
from wikiscraper.scraper.wiki_api import get_all_revisions


def get_new_revisions(page: str) -> list[Revision]:
    existing_revisions = get_stored_revisions(page)
    print(type(existing_revisions[0].date))
    latest_revision_date: datetime.datetime = max(
        rev.date for rev in existing_revisions
    )
    print(f"Latest revision date is {latest_revision_date}")
    return get_all_revisions(
        page, latest_revision_date
    )  # This still gives the last revision we have, but we can filter it out later


if __name__ == "__main__":
    for page_title in ["Lego", "Lego Star Wars"]:
        print(f"Getting new revisions for {page_title}")
        new_revisions = get_new_revisions(page_title)
        print(f"Getting new contributors for {page_title}")
        new_contributors = get_contributors_from_revisions(
            new_revisions
        )  # upsert them into the database
        print(
            f"Found {len(new_revisions)} new revisions and {len(new_contributors)} new contributors"
        )
