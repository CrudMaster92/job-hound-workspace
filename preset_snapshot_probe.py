"""Read-only preview acceptance probe; no scraper runs or user-profile writes."""
from __future__ import annotations
import json
from pathlib import Path
import tempfile
from unittest.mock import patch
import socket

import sys
sys.path.insert(0, str(Path.cwd()))
from server.app import create_app
from server.presets import CatalogSelectionRequest


def main():
    with tempfile.TemporaryDirectory(prefix="jobhound-preset-probe-") as temporary:
        app = create_app(db_path=Path(temporary) / "db.sqlite3", start_scheduler=False, seed_default_documents=False)
        with patch("socket.getaddrinfo", return_value=[(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("198.18.138.37", 443))]):
            listing = app.state.presets.list_presets(force_refresh=True)
            ids = {item["id"] for item in listing["items"]}
            assert {"ai", "fortune-50-2026", "gaming", "marketing-agencies-canada", "recruitment-agencies-north-america"} <= ids
            assert listing["catalog_source"] == "release_snapshot" and listing["catalog_status"] == "stale"
            detail = app.state.presets.get_preset_page("marketing-agencies-canada", limit=100)
            assert len(detail["companies"]) > 0
            page = app.state.presets.search_catalog_companies(collection_id="marketing-agencies-canada", limit=100)
            assert page["total"] == detail["company_count"]
            first = detail["companies"][0]
            catalog = app.state.presets.catalog_client
            members = catalog.get_collection_members("marketing-agencies-canada")
            reference = next(monitor for member in members for monitor in member.get("monitors", []))
            assert catalog.get_monitor(reference, force=True)["recipe"]
            company_id = next(member["company_id"] for member in members if reference in member.get("monitors", []))
            preview = app.state.presets.preview_catalog_selection(CatalogSelectionRequest(
                format="jobhound-catalog-install", version=1, catalog_version=3,
                source_commit=listing["source_commit"], mode="collection", collection_id="marketing-agencies-canada",
                selections=[{"company_id": company_id, "monitor_id": reference["id"], "revision": reference["revision"]}]))
            assert preview["count"] == 1 and not preview["unavailable"]
            assert app.state.db.list_companies() == [] and app.state.db.list_runs() == []
            print(json.dumps({"ok": True, "check": "packaged_full_catalog_with_synthetic_dns", "collections": sorted(ids), "marketing_companies": page["total"], "marketing_monitors": len(detail["companies"])}))


if __name__ == "__main__":
    main()
