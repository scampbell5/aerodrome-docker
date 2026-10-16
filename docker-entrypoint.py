#!/usr/bin/env python3

import os
import shutil
import sys
from pathlib import Path

import yaml

APP_DIR = Path("/opt/aerodrome")
DATA_DIR = Path("/data")
DATA_CONFIG = DATA_DIR / "config.yaml"
APP_CONFIG = APP_DIR / "config.yaml"
EXAMPLE_CONFIG = APP_DIR / "config.yaml.example"


def set_if_present(mapping, key, env_name, caster=str):
    value = os.getenv(env_name)
    if value is None or value == "":
        return
    mapping[key] = caster(value)


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "logs").mkdir(parents=True, exist_ok=True)

    if not DATA_CONFIG.exists():
        shutil.copy2(EXAMPLE_CONFIG, DATA_CONFIG)

    with DATA_CONFIG.open("r", encoding="utf-8") as fh:
        config = yaml.safe_load(fh) or {}

    receiver = config.setdefault("receiver", {})
    receiver["ip"] = os.getenv("RECEIVER_HOST", receiver.get("ip", "piaware"))
    receiver["port"] = int(os.getenv("RECEIVER_PORT", receiver.get("port", 80)))
    receiver["path"] = os.getenv("RECEIVER_PATH", receiver.get("path", "/data/aircraft.json"))
    receiver["poll_interval"] = int(os.getenv("RECEIVER_POLL_INTERVAL", receiver.get("poll_interval", 60)))
    receiver["distance_unit"] = os.getenv("DISTANCE_UNIT", receiver.get("distance_unit", "nmi"))
    receiver["track_link_provider"] = os.getenv("TRACK_LINK_PROVIDER", receiver.get("track_link_provider", "flightaware"))
    set_if_present(receiver, "latitude", "RECEIVER_LATITUDE", float)
    set_if_present(receiver, "longitude", "RECEIVER_LONGITUDE", float)

    web = config.setdefault("web", {})
    web["host"] = "0.0.0.0"
    web["port"] = 8000

    data = config.setdefault("data", {})
    data["db_file"] = "/data/aircraft_history.db"

    logging_cfg = config.setdefault("logging", {})
    logging_cfg["dir"] = "/data/logs"

    stats = config.setdefault("stats", {})
    stats["timezone"] = os.getenv("STATS_TIMEZONE", os.getenv("TZ", stats.get("timezone", "")))

    # Container images are updated by rebuilding/redeploying from Portainer.
    # Keep Aerodrome's in-app updater disabled so it doesn't try to mutate
    # the ephemeral container filesystem.
    updates = config.setdefault("updates", {}).setdefault("github", {})
    updates["enabled"] = False

    with DATA_CONFIG.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(config, fh, sort_keys=False, allow_unicode=True)

    if APP_CONFIG.exists() or APP_CONFIG.is_symlink():
        APP_CONFIG.unlink()
    APP_CONFIG.symlink_to(DATA_CONFIG)

    os.chdir(APP_DIR)
    os.execvp(sys.argv[1], sys.argv[1:])


if __name__ == "__main__":
    main()
