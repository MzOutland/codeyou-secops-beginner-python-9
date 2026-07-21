import argparse

from inventory_manager import InventoryManager
from inventory_source import (
    CrowdstrikeInventorySource,
    NetboxInventorySource,
    QualysInventorySource,
)


NETBOX_API_URL = (
    "https://my.api.mockaroo.com/"
    "ironclad/netbox/inventory.json"
)

QUALYS_API_URL = (
    "https://my.api.mockaroo.com/"
    "ironclad/qualys/inventory.json"
)

CROWDSTRIKE_API_URL = (
    "https://my.api.mockaroo.com/"
    "ironclad/crowdstrike/inventory.json"
)


def build_manager() -> InventoryManager:
    sources = {
        "netbox": NetboxInventorySource(
            NETBOX_API_URL
        ),
        "qualys": QualysInventorySource(
            QUALYS_API_URL
        ),
        "crowdstrike": CrowdstrikeInventorySource(
            CROWDSTRIKE_API_URL
        ),
    }

    return InventoryManager(sources)


def cmd_pull(args) -> None:
    manager = build_manager()
    manager.pull(args.source)

    print("Pulled inventory.")
    print("Stats:", manager.stats())


def cmd_list(args) -> None:
    manager = build_manager()
    manager.pull(args.source)

    for asset in manager.list_assets(args.source):
        print(asset.summary())


def cmd_search(args) -> None:
    manager = build_manager()
    manager.pull(args.source)

    results = manager.search(
        args.query,
        args.source
    )

    print(f"Results: {len(results)}")

    for asset in results[:args.limit]:
        print(asset.summary())


def cmd_stats(args) -> None:
    manager = build_manager()
    manager.pull(args.source)

    print("Stats:", manager.stats())


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="ironclad-inventory",
        description="Ironclad Unified Inventory CLI",
    )

    subparsers = parser.add_subparsers(
        dest="cmd",
        required=True,
    )

    pull_parser = subparsers.add_parser(
        "pull",
        help="Pull inventory from a source",
    )

    pull_parser.add_argument(
        "--source",
        choices=[
            "netbox",
            "qualys",
            "crowdstrike",
            "all",
        ],
        default="all",
    )

    pull_parser.set_defaults(func=cmd_pull)

    list_parser = subparsers.add_parser(
        "list",
        help="List assets",
    )

    list_parser.add_argument(
        "--source",
        choices=[
            "netbox",
            "qualys",
            "crowdstrike",
            "all",
        ],
        default="all",
    )

    list_parser.set_defaults(func=cmd_list)

    search_parser = subparsers.add_parser(
        "search",
        help="Search assets by keyword",
    )

    search_parser.add_argument(
        "--source",
        choices=[
            "netbox",
            "qualys",
            "crowdstrike",
            "all",
        ],
        default="all",
    )

    search_parser.add_argument(
        "--query",
        required=True,
    )

    search_parser.add_argument(
        "--limit",
        type=int,
        default=50,
    )

    search_parser.set_defaults(func=cmd_search)

    stats_parser = subparsers.add_parser(
        "stats",
        help="Show counts by source",
    )

    stats_parser.add_argument(
        "--source",
        choices=[
            "netbox",
            "qualys",
            "crowdstrike",
            "all",
        ],
        default="all",
    )

    stats_parser.set_defaults(func=cmd_stats)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
    