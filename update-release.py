#!/usr/bin/env python3

from datetime import datetime
import json
import hashlib
import requests
import sys
from lxml import etree

ENDPOINT = "https://api.snapcraft.io/v2/snaps/info/spotify"
MANIFEST = "com.spotify.Client.json"
APPDATA = "com.spotify.Client.appdata.xml"
HEADERS = {"Snap-Device-Series": "16"}


def fetch_snap_info(endpoint, headers):
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get snap info, status code: {response.status_code}")
        print(f"Response: {response.text}")
        sys.exit()


def calculate_sha256(url):
    sha256_hash = hashlib.sha256()
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        for chunk in response.iter_content(chunk_size=1024):
            sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
    else:
        print(f"Failed to download the file, status code: {response.status_code}")
        print(f"Response: {response.text}")
        sys.exit()


def update_manifest(extracted_data, channel):
    with open(MANIFEST, "r") as f:
        data = json.load(f)

    for module in data.get("modules", []):
        if module.get("name") == "spotify":
            for source in module.get("sources", []):
                if source.get("type") == "extra-data":
                    if source["url"] == extracted_data[channel]["url"]:
                        print("Already up to date")
                        sys.exit()
                    source["url"] = extracted_data[channel]["url"]
                    source["sha256"] = calculate_sha256(extracted_data[channel]["url"])
                    source["size"] = extracted_data[channel]["size"]
                    break

    with open(MANIFEST, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Updated manifest for {channel}, please test")
    update_appdata(extracted_data, channel)


def update_appdata(extracted_data, channel):
    parser = etree.XMLParser(remove_comments=False)
    tree = etree.parse(APPDATA, parser=parser)
    date_str = extracted_data[channel]["date"]
    parsed_date = datetime.fromisoformat(date_str)
    formatted_date = parsed_date.strftime("%Y-%m-%d")
    release = etree.Element(
        "release",
        {
            "version": extracted_data[channel]["version"],
            "date": formatted_date,  # Use the formatted date
        },
    )
    releases = tree.find("releases")
    release.tail = "\n    "
    releases.insert(0, release)
    tree.write(APPDATA, xml_declaration=True, encoding="utf-8")
    print(f"Updated appdata for {channel}, ensure its correct")


def main(channel="stable"):
    snap_info = fetch_snap_info(ENDPOINT, HEADERS)
    extracted_data = {}
    for channel_info in snap_info["channel-map"]:
        risk = channel_info["channel"]["risk"]
        extracted_data[risk] = {
            "date": channel_info["channel"]["released-at"],
            "sha3-384": channel_info["download"]["sha3-384"],
            "url": channel_info["download"]["url"],
            "size": channel_info["download"]["size"],
            "version": channel_info["version"],
        }
    if channel not in extracted_data:
        print(f"The channel {channel} is not found.")
        sys.exit()

    update_manifest(extracted_data, channel)


if __name__ == "__main__":
    # You could replace 'stable' with another channel if needed.
    main(channel="stable")
