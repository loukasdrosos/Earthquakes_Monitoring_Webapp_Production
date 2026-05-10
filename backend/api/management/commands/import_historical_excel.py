import re
from datetime import datetime, timezone as dt_timezone

import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from api.models import Earthquake


MONTHS = {
    "JAN": 1,
    "FEB": 2,
    "MAR": 3,
    "APR": 4,
    "MAY": 5,
    "JUN": 6,
    "JUL": 7,
    "AUG": 8,
    "SEP": 9,
    "OCT": 10,
    "NOV": 11,
    "DEC": 12,
}


def parse_earthquake_line(line):
    line = str(line).strip()

    pattern = re.compile(
        r"^\s*"
        r"(?P<year>\d{4})\s+"
        r"(?P<month>[A-Za-z]{3})\s+"
        r"(?P<day>\d{1,2})\s+"
        r"(?P<hour>\d{1,2})\s+"
        r"(?P<minute>\d{1,2})\s+"
        r"(?P<second>\d{1,2}(?:\.\d+)?)\s+"
        r"(?P<latitude>-?\d+(?:\.\d+)?)\s+"
        r"(?P<longitude>-?\d+(?:\.\d+)?)\s+"
        r"(?P<depth>-?\d+(?:\.\d+)?)\s+"
        r"(?P<magnitude>-?\d+(?:\.\d+)?)"
        r"\s*$"
    )

    match = pattern.match(line)

    if not match:
        raise ValueError(f"Line does not match expected format: {line}")

    data = match.groupdict()

    month_text = data["month"].upper()

    if month_text not in MONTHS:
        raise ValueError(f"Unknown month: {month_text}")

    second_float = float(data["second"])
    second = int(second_float)
    microsecond = int(round((second_float - second) * 1_000_000))

    dt = datetime(
        int(data["year"]),
        MONTHS[month_text],
        int(data["day"]),
        int(data["hour"]),
        int(data["minute"]),
        second,
        microsecond,
    )

    aware_dt = timezone.make_aware(dt, timezone=dt_timezone.utc)

    return Earthquake(
        time=aware_dt,
        latitude=round(float(data["latitude"]), 4),
        longitude=round(float(data["longitude"]), 4),
        depth=float(data["depth"]),
        magnitude=float(data["magnitude"]),
    )


class Command(BaseCommand):
    help = "Import historical earthquake data from an Excel file."

    def add_arguments(self, parser):
        parser.add_argument("excel_path", type=str)

    def handle(self, *args, **options):
        excel_path = options["excel_path"]

        try:
            df = pd.read_excel(excel_path, header=None, engine="openpyxl")
        except FileNotFoundError:
            raise CommandError(f"Excel file not found: {excel_path}")

        earthquakes = []
        skipped_count = 0
        errors = []

        total_rows = len(df)

        self.stdout.write(f"Reading {total_rows} Excel rows...")

        for row_number, row in df.iterrows():
            line = " ".join(
                str(value).strip()
                for value in row.tolist()
                if pd.notna(value) and str(value).strip()
            )

            if not line:
                skipped_count += 1
                continue

            upper_line = line.upper()

            if (
                "DATE" in upper_line
                or "TIME" in upper_line
                or "LAT" in upper_line
                or "LONG" in upper_line
                or "GMT" in upper_line
                or "LOCAL" in upper_line
            ):
                skipped_count += 1
                continue

            try:
                earthquake = parse_earthquake_line(line)
                earthquakes.append(earthquake)
            except Exception as exc:
                errors.append(f"Excel row {row_number + 1}: {exc}")

            if row_number % 5000 == 0:
                self.stdout.write(f"Parsed {row_number}/{total_rows} rows...")

        self.stdout.write(f"Parsed earthquakes: {len(earthquakes)}")
        self.stdout.write("Saving to database...")

        Earthquake.objects.bulk_create(
            earthquakes,
            ignore_conflicts=True,
            batch_size=1000,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Import complete. Parsed: {len(earthquakes)}, "
                f"Skipped: {skipped_count}, "
                f"Errors: {len(errors)}"
            )
        )

        for error in errors[:30]:
            self.stderr.write(error)