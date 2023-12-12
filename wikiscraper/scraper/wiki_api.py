import logging
from datetime import datetime

import requests
from wikiscraper.scraper.data_mappings import Revision

BASE_REQUEST = {
    "action": "query",
    "formatversion": "2",
    "format": "json",
}

BASE_REVISION_REQUEST = dict(
    BASE_REQUEST,
    **{
        "prop": "revisions",
        "rvslots": "main",
        "rvdir": "newer",
    },
)

logger = logging.getLogger(__name__)


def query(request):
    last_continue = {}
    while True:
        # Clone original request
        req = request.copy()
        # Modify it with the values returned in the 'continue' section of the last result.
        req.update(last_continue)
        # Call API
        result = requests.get(
            "https://en.wikipedia.org/w/api.php", params=req, timeout=120
        ).json()
        if "error" in result:
            raise RuntimeError(result["error"])
        if "warnings" in result:
            logger.warning(result["warnings"])
        if "query" in result:
            yield result["query"]
        if "continue" not in result:
            break
        last_continue = result["continue"]


def get_all_revisions(page_title: str, start_date: datetime) -> list[Revision]:
    logger.info(f"Getting all revisions for {page_title} starting from {start_date}")
    params = dict(
        BASE_REVISION_REQUEST,
        **{
            "titles": page_title,
            "rvlimit": "500",
            "rvprop": "ids|userid|timestamp|tags",
            "rvstart": start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        },
    )
    revisions: list[Revision] = list[Revision]()
    for result in query(params):
        pages = result["pages"]
        for page in pages:
            for rev in page["revisions"]:
                revisions.append(
                    Revision(rev["revid"], rev["userid"], rev["timestamp"], rev["tags"])
                )
    return revisions


def get_users_info(user_ids: list[int]):
    logger.warning("Getting info for users")
    assert len(user_ids) <= 50, "The maximum number of users that can be queried is 50"
    params = dict(
        BASE_REQUEST,
        **{
            "list": "users",
            "usprop": "blockinfo|groups|editcount|registration|emailable|gender|centralids|cancreate",
            "ususerids": "|".join([str(user_id) for user_id in user_ids]),
        },
    )
    all_users: list[dict] = list[dict]()
    for result in query(params):
        users = result["users"]
        all_users.extend(users)
    return all_users
