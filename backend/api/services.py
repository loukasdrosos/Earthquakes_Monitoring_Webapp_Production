import csv
import os
import re
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

from django.utils import timezone

from .models import Earthquake


def parse_earthquake_description(description):
    cleaned_desc = description.replace("<br>", "\n")

    time_match = re.search(
        r"Time:\s*(\d{2}-[A-Za-z]{3}-\d{4} \d{2}:\d{2}:\d{2})",
        cleaned_desc
    )
    lat_match = re.search(r"Latitude:\s*([\d.]+)N", cleaned_desc)
    lon_match = re.search(r"Longitude:\s*([\d.]+)E", cleaned_desc)
    depth_match = re.search(r"Depth:\s*([\d.]+)km", cleaned_desc)
    mag_match = re.search(r"M\s*([\d.]+)", cleaned_desc)

    if not all([time_match, lat_match, lon_match, depth_match, mag_match]):
        raise ValueError("Could not find all earthquake fields in description.")

    earthquake_time = timezone.make_aware(
        datetime.strptime(time_match.group(1), "%d-%b-%Y %H:%M:%S")
    )

    return {
        "time": earthquake_time,
        "latitude": float(lat_match.group(1)),
        "longitude": float(lon_match.group(1)),
        "depth": float(depth_match.group(1)),
        "magnitude": float(mag_match.group(1)),
    }


def save_earthquake(data):
    earthquake, created = Earthquake.objects.get_or_create(
        time=data["time"],
        latitude=data["latitude"],
        longitude=data["longitude"],
        depth=data["depth"],
        magnitude=data["magnitude"],
    )

    return earthquake, created


def fetch_and_save_earthquakes_from_xml():
    url = os.getenv("DATA_FETCH_URL", "")

    if not url:
        raise ValueError("DATA_FETCH_URL is not configured.")

    response = requests.get(url, timeout=20)
    response.raise_for_status()

    root = ET.fromstring(response.content)

    created_count = 0
    existing_count = 0
    errors = []

    for item in root.findall(".//item"):
        try:
            description_element = item.find("description")

            if description_element is None or not description_element.text:
                raise ValueError("Missing description field.")

            data = parse_earthquake_description(description_element.text)
            _, created = save_earthquake(data)

            if created:
                created_count += 1
            else:
                existing_count += 1

        except Exception as exc:
            errors.append(str(exc))

    return {
        "created": created_count,
        "existing": existing_count,
        "errors": errors,
    }