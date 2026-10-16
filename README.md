# Aerodrome Docker for Portainer

Portainer-friendly Docker wrapper for Preston Peterson's Aerodrome ADS-B dashboard.

## Design

- Builds Aerodrome `v3.4.136` from the upstream release source.
- Uses the public `python:3.13-slim-bookworm` image; no `dhi.io` authentication.
- Exposes Aerodrome on host port `7070`.
- Connects to the existing external Docker network `adsb-net`.
- Reads PiAware at `http://piaware:80/data/aircraft.json`.
- Persists `config.yaml`, SQLite history, and logs in the `aerodrome-data` volume.
- Disables Aerodrome's in-app updater; update by changing `AERODROME_REF` and redeploying.

## Portainer deployment

Create/deploy a Git Repository stack with:

- Repository: `https://github.com/scampbell5/aerodrome-docker.git`
- Reference: `main`
- Compose path: `docker-compose.yml`

Set these Stack environment variables in Portainer rather than committing coordinates to GitHub:

- `RECEIVER_LATITUDE`
- `RECEIVER_LONGITUDE`

Then deploy and open:

`http://YOUR_OMV_IP:7070`

The `adsb-net` network must already exist, and the PiAware container must also be attached to it with the DNS/container name `piaware`.
