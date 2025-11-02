# Bengaluru Metro Stations Database
# Structure mirrors `hyderabad_metro_stations.py`, adapted for Bengaluru.
# Station coordinates and place_ids are loaded from the generated CSV
# `bengaluru_station_coords_full.csv` (created earlier via Google Places).

from __future__ import annotations


# Lines with accurate, finalized sequences
METRO_LINES = {
    'Purple Line': {
        'name': 'Purple Line',
        'stations': [
            "Whitefield (Kadugodi)", "Hopefarm Channasandra", "Kadugodi Tree Park",
            "Pattandur Agrahara", "Sri Sathya Sai Hospital", "Nallurhalli",
            "Kundalahalli", "Seetharamapalya", "Hoodi", "Garudacharpalya",
            "Singayyanapalya", "Krishnarajapura", "Benniganahalli", "Baiyappanahalli",
            "Swami Vivekananda Road", "Indiranagar", "Halasuru", "Trinity",
            "Mahatma Gandhi Road", "Cubbon Park", "Dr. B. R. Ambedkar Station, Vidhana Soudha",
            "Sir M. Visvesvaraya Station, Central College", "Nadaprabhu Kempegowda Station, Majestic",
            "Krantivira Sangolli Rayanna Railway Station", "Magadi Road",
            "Sri Balagangadharanatha Swamiji Station, Hosahalli", "Vijayanagar", "Attiguppe",
            "Deepanjali Nagar", "Mysuru Road", "Pantharapalya–Nayandahalli", "Rajarajeshwari Nagar",
            "Jnanabharathi", "Pattanagere", "Kengeri Bus Terminal", "Kengeri", "Challaghatta",
        ],
    },
    'Green Line': {
        'name': 'Green Line',
        'stations': [
            "Madavara", "Chikkabidarakallu", "Manjunathanagara", "Nagasandra", "Dasarahalli",
            "Jalahalli", "Peenya Industry", "Peenya", "Goraguntepalya", "Yeshwanthpur",
            "Sandal Soap Factory", "Mahalakshmi", "Rajajinagar", "Mahakavi Kuvempu Road",
            "Srirampura", "Mantri Square Sampige Road", "Nadaprabhu Kempegowda Station, Majestic",
            "Chickpete", "Krishna Rajendra Market", "National College", "Lalbagh", "South End Circle",
            "Jayanagar", "Rashtreeya Vidyalaya Road", "Banashankari", "Jaya Prakash Nagar",
            "Yelachenahalli", "Konanakunte Cross", "Doddakallasandra", "Vajarahalli",
            "Thalaghattapura", "Silk Institute",
        ],
    },
    'Yellow Line': {
        'name': 'Yellow Line',
        'stations': [
            "Rashtreeya Vidyalaya Road", "Ragigudda", "Jayadeva Hospital", "BTM Layout",
            "Central Silk Board", "Bommanahalli", "Hongasandra", "Kudlu Gate", "Singasandra",
            "Hosa Road", "Beratena Agrahara", "Electronic City",
            "Infosys Foundation Konappana Agrahara", "Huskur Road", "Biocon Hebbagodi",
            "Delta Electronics Bommasandra",
        ],
    },
}


# Unique station list (order not guaranteed as we deduplicate)
ALL_STATIONS = []
_seen = set()
for corridor in METRO_LINES.values():
    for station in corridor['stations']:
        if station not in _seen:
            _seen.add(station)
            ALL_STATIONS.append(station)


# Interchanges (Bengaluru has only two at present)
INTERCHANGE_STATIONS = {
    'Nadaprabhu Kempegowda Station, Majestic': ['Purple Line', 'Green Line'],
    'Rashtreeya Vidyalaya Road': ['Green Line', 'Yellow Line'],
}


# System parameters (researched defaults; can be tuned)
BENGALURU_METRO_CHARACTERISTICS = {
    'total_corridors': 3,
    'avg_speed_kmph': 33,               # typical operational average
    'dwell_time_s': 25,                 # most stations 20–30s; Majestic may be higher
    'interchange_time_minutes_default': 5,
    'interchange_time_minutes_overrides': {
        'Nadaprabhu Kempegowda Station, Majestic': 6,
        'Rashtreeya Vidyalaya Road': 4,
    },
    'headway_minutes_peak': 4.5,
    'headway_minutes_offpeak': 8.0,
}

# Hardcoded coordinates and place_ids (sourced from bengaluru_station_coords_full.csv)
STATION_COORDINATES = {
    "Whitefield (Kadugodi)": (12.995626, 77.75780499999999),
    "Hopefarm Channasandra": (12.987348, 77.753796),
    "Kadugodi Tree Park": (12.985711, 77.746842),
    "Pattandur Agrahara": (12.987622, 77.737737),
    "Sri Sathya Sai Hospital": (12.98122, 77.72753999999999),
    "Nallurhalli": (12.976632, 77.724752),
    "Kundalahalli": (12.977607, 77.71552299999999),
    "Seetharamapalya": (12.9808333, 77.70883549999999),
    "Hoodi": (12.988782, 77.711364),
    "Garudacharpalya": (12.993482, 77.70365799999999),
    "Singayyanapalya": (12.996557, 77.692708),
    "Krishnarajapura": (12.999922, 77.677607),
    "Benniganahalli": (12.9963737, 77.6682628),
    "Baiyappanahalli": (12.98959, 77.65366),
    "Swami Vivekananda Road": (12.9859106, 77.645004),
    "Indiranagar": (12.9782619, 77.63852570000002),
    "Halasuru": (12.9763635, 77.62671499999999),
    "Trinity": (12.973342, 77.615719),
    "Mahatma Gandhi Road": (12.9755162, 77.6066919),
    "Cubbon Park": (12.9809008, 77.59746539999999),
    "Dr. B. R. Ambedkar Station, Vidhana Soudha": (12.9796925, 77.5926343),
    "Sir M. Visvesvaraya Station, Central College": (12.9742805, 77.5839458),
    "Nadaprabhu Kempegowda Station, Majestic": (12.975692, 77.572844),
    "Krantivira Sangolli Rayanna Railway Station": (12.9758403, 77.5657561),
    "Magadi Road": (12.9756582, 77.55541149999999),
    "Sri Balagangadharanatha Swamiji Station, Hosahalli": (12.9742975, 77.5454436),
    "Vijayanagar": (12.9708197, 77.5373638),
    "Attiguppe": (12.9621018, 77.5337131),
    "Deepanjali Nagar": (12.952215, 77.5371013),
    "Mysuru Road": (12.9467268, 77.53007389999999),
    "Pantharapalya–Nayandahalli": (12.946231, 77.52985),
    "Rajarajeshwari Nagar": (12.936693, 77.519556),
    "Jnanabharathi": (12.935446, 77.51217799999999),
    "Pattanagere": (12.924276, 77.498305),
    "Kengeri Bus Terminal": (12.914642, 77.487704),
    "Kengeri": (12.9078282, 77.47636670000001),
    "Challaghatta": (12.8973787, 77.4612408),
    "Madavara": (13.0573826, 77.47295969999999),
    "Chikkabidarakallu": (13.052417, 77.487894),
    "Manjunathanagara": (13.050155, 77.494377),
    "Nagasandra": (13.0481133, 77.5001231),
    "Dasarahalli": (13.0435419, 77.51237909999999),
    "Jalahalli": (13.0395842, 77.51983779999999),
    "Peenya Industry": (13.0363672, 77.52552039999999),
    "Peenya": (13.0329869, 77.53346909999999),
    "Goraguntepalya": (13.028486, 77.5408673),
    "Yeshwanthpur": (13.0233093, 77.5498636),
    "Sandal Soap Factory": (13.0148546, 77.5545643),
    "Mahalakshmi": (13.0083376, 77.5488342),
    "Rajajinagar": (13.0003458, 77.54974829999999),
    "Mahakavi Kuvempu Road": (12.9985023, 77.5569472),
    "Srirampura": (12.9965258, 77.5633563),
    "Mantri Square Sampige Road": (12.9905452, 77.5708049),
    "Chickpete": (12.9675461, 77.5747925),
    "Krishna Rajendra Market": (12.960161, 77.574479),
    "National College": (12.9506135, 77.5737362),
    "Lalbagh": (12.946287, 77.5800611),
    "South End Circle": (12.9383208, 77.58007479999999),
    "Jayanagar": (12.9296749, 77.5801753),
    "Rashtreeya Vidyalaya Road": (12.9215877, 77.5802611),
    "Banashankari": (12.9155385, 77.5736288),
    "Jaya Prakash Nagar": (12.9075563, 77.573061),
    "Yelachenahalli": (12.8960529, 77.5701606),
    "Konanakunte Cross": (12.888909, 77.56277999999999),
    "Doddakallasandra": (12.884636, 77.552824),
    "Vajarahalli": (12.877485, 77.544817),
    "Thalaghattapura": (12.871366, 77.538439),
    "Silk Institute": (12.861672, 77.52998099999999),
    "Ragigudda": (12.9170037, 77.58833589999999),
    "Jayadeva Hospital": (12.9167331, 77.6000931),
    "BTM Layout": (12.916488, 77.60806099999999),
    "Central Silk Board": (12.9164445, 77.62052609999999),
    "Bommanahalli": (12.9107316, 77.62632789999999),
    "Hongasandra": (12.9017117, 77.6319874),
    "Kudlu Gate": (12.8900206, 77.63918190000001),
    "Singasandra": (12.8808676, 77.6447379),
    "Hosa Road": (12.8701588, 77.65275489999999),
    "Beratena Agrahara": (12.863676, 77.65789699999999),
    "Electronic City": (12.8562351, 77.6637798),
    "Infosys Foundation Konappana Agrahara": (12.84626, 77.67114699999999),
    "Huskur Road": (12.838885, 77.677433),
    "Biocon Hebbagodi": (12.828967, 77.681405),
    "Delta Electronics Bommasandra": (12.8193154, 77.68834009999999),
}

STATION_PLACE_IDS = {
    "Whitefield (Kadugodi)": "ChIJOdwilxcOrjsR-6MvlsusM00",
    "Hopefarm Channasandra": "ChIJMRmA3xoOrjsRCp8oIXTX9RM",
    "Kadugodi Tree Park": "ChIJS_ojywIOrjsRVtyLn4BoNnw",
    "Pattandur Agrahara": "ChIJ1-At8uQRrjsRU3foUV135ok",
    "Sri Sathya Sai Hospital": "ChIJr5Fc2vMRrjsRF4WM58uQkS4",
    "Nallurhalli": "ChIJx9bz-_QRrjsRNU3ib6xyMXs",
    "Kundalahalli": "ChIJRWICRIkRrjsRw99Xm5WFyhY",
    "Seetharamapalya": "ChIJsUHA1f8RrjsRsk2ztqTF2kQ",
    "Hoodi": "ChIJCyddpJARrjsRKnXrc3LZVNk",
    "Garudacharpalya": "ChIJnytwFZ8RrjsR4oh_mLMrb4U",
    "Singayyanapalya": "ChIJARDqkQwRrjsRv9n3wCZVhgo",
    "Krishnarajapura": "ChIJ6yYmDBYRrjsR-XAcsParqj4",
    "Benniganahalli": "ChIJ6eHf9mARrjsR274ajmNxxh0",
    "Baiyappanahalli": "ChIJh00lK0sRrjsRpsciq16fZ6Y",
    "Swami Vivekananda Road": "ChIJP-ri17AWrjsROiCDxVe3X74",
    "Indiranagar": "ChIJZbZd-qQWrjsRe7G5a9GUZ9U",
    "Halasuru": "ChIJSd03apkWrjsRmpKnR3Cq5Ck",
    "Trinity": "ChIJQfmchYMWrjsR3ETTlmpjx0I",
    "Mahatma Gandhi Road": "ChIJvwy9o30WrjsR_3Soez0XLL8",
    "Cubbon Park": "ChIJdUZ_eWUWrjsRfo6CcEaixkU",
    "Dr. B. R. Ambedkar Station, Vidhana Soudha": "ChIJ-wIASG4WrjsRaLxJGOEWl2c",
    "Sir M. Visvesvaraya Station, Central College": "ChIJmR7YxQwWrjsRW5vq4ycsdm4",
    "Nadaprabhu Kempegowda Station, Majestic": "ChIJZQRCbwUWrjsRko0PHW2ZX6k",
    "Krantivira Sangolli Rayanna Railway Station": "ChIJzZmnPQMWrjsRhEgM3qcVawM",
    "Magadi Road": "ChIJybGxEPo9rjsRvVr1TcQEmxo",
    "Sri Balagangadharanatha Swamiji Station, Hosahalli": "ChIJT50hxeU9rjsRlPxnxhLf-Vc",
    "Vijayanagar": "ChIJyzrM3N09rjsRqiGadttypE4",
    "Attiguppe": "ChIJmV4y0XU-rjsRzclMF8nLs0I",
    "Deepanjali Nagar": "ChIJ7YKrb20-rjsRWuc27yLlYHE",
    "Mysuru Road": "ChIJycE_0Gg-rjsRJVmVnabEF2Q",
    "Pantharapalya–Nayandahalli": "ChIJFzIC22g-rjsRI_CMVvZhmHU",
    "Rajarajeshwari Nagar": "ChIJLb5o3V4-rjsRJH2aID0lcCQ",
    "Jnanabharathi": "ChIJW85xJPQ-rjsRvv7Jifc2tXE",
    "Pattanagere": "ChIJu6v7ouY-rjsRo6QAv0TU7CQ",
    "Kengeri Bus Terminal": "ChIJG4890iA_rjsRAC5w3leOUow",
    "Kengeri": "ChIJ1U1wr3Y_rjsROkbeYesRWD0",
    "Challaghatta": "ChIJG87IxFo5rjsRvxo6f6Mh12Y",
    "Madavara": "ChIJb2MVG5EjrjsRjMVAmK9SkOw",
    "Chikkabidarakallu": "ChIJ68zPrLQ8rjsRQyyb4MFH6lo",
    "Manjunathanagara": "ChIJH8Goi8o8rjsROOlpepJgnyk",
    "Nagasandra": "ChIJq1azIsw8rjsR5hvX2pEeE_k",
    "Dasarahalli": "ChIJZYE0XtQ8rjsRu5QJhqVvIHc",
    "Jalahalli": "ChIJk85Oqic9rjsR6eUJsEOTTdQ",
    "Peenya Industry": "ChIJCSQ8biM9rjsRfNnuMYSSc7s",
    "Peenya": "ChIJJwvQCT49rjsRNGFfWIOuPzM",
    "Goraguntepalya": "ChIJ__-_Ems9rjsRcxA1KnoFxLE",
    "Yeshwanthpur": "ChIJ78lSjG89rjsRJKXpBHA_dcU",
    "Sandal Soap Factory": "ChIJE40mbXk9rjsRYWzw7saYk-E",
    "Mahalakshmi": "ChIJ6czjFp09rjsRX4p6ip6inSY",
    "Rajajinagar": "ChIJecUIuJo9rjsRCPx6gSQcYWM",
    "Mahakavi Kuvempu Road": "ChIJn3ibuog9rjsRPN0hN4eLeBA",
    "Srirampura": "ChIJY1GVdCcWrjsR0pLwnGCUmKc",
    "Mantri Square Sampige Road": "ChIJy2aM9iIWrjsRPRgNzAqF9mo",
    "Chickpete": "ChIJ-7zgFwgWrjsRe_Sgg1nXcV4",
    "Krishna Rajendra Market": "ChIJfUzCNeUVrjsR22xhBdxVF_I",
    "National College": "ChIJpdMgH-4VrjsRLMrgPnksIvs",
    "Lalbagh": "ChIJFZ7lcOsVrjsRpI3gtGXhbdc",
    "South End Circle": "ChIJUeZ3HZQVrjsRYSbTWxcLXZI",
    "Jayanagar": "ChIJ6zSXdpkVrjsRvb2SqkmrHBc",
    "Rashtreeya Vidyalaya Road": "ChIJGymEHp4VrjsRR5cYC8E5tWM",
    "Banashankari": "ChIJFfoeVXcVrjsRUKMZuV47coQ",
    "Jaya Prakash Nagar": "ChIJCwCOfGUVrjsRkNcI9wbOo4Q",
    "Yelachenahalli": "ChIJezEhr10VrjsR8Kkc4v3gXeo",
    "Konanakunte Cross": "ChIJG1zkZFgVrjsRVMu8W6Vku88",
    "Doddakallasandra": "ChIJVb525_o_rjsROC03DtIp6ak",
    "Vajarahalli": "ChIJEWbGgfY_rjsR45lwRFCiNx8",
    "Thalaghattapura": "ChIJJ90wKHVArjsR-RJA4w2YfnE",
    "Silk Institute": "ChIJ3R4Xzm9ArjsROzhpuVg2fho",
    "Ragigudda": "ChIJx9Z8dQAVrjsRDKWBrI6O0_Y",
    "Jayadeva Hospital": "ChIJL-fqRwAVrjsRO5ziy-KDOLc",
    "BTM Layout": "ChIJC2hz-f0UrjsRc0WcLXUKXMI",
    "Central Silk Board": "ChIJl8NMAwAVrjsRvop90Vobkvk",
    "Bommanahalli": "ChIJweJ3eZcVrjsRvWO5l55NnB0",
    "Hongasandra": "ChIJS8127RkVrjsRAAwS7NLZMzc",
    "Kudlu Gate": "ChIJIakSxv8VrjsR_uXLc2Ykep0",
    "Singasandra": "ChIJ2U-TVpYVrjsRozMWw2GpFiI",
    "Hosa Road": "ChIJuxhHXABrrjsRpr4dxIc4U0o",
    "Beratena Agrahara": "ChIJcQD1x6ZsrjsRfxn6LH0Rfv4",
    "Electronic City": "ChIJdwCsOsZtrjsRnOwQj5-fdAY",
    "Infosys Foundation Konappana Agrahara": "ChIJ8dqs_o1srjsR6g5x43RGVag",
    "Huskur Road": "ChIJRy2y2_RsrjsRnL3f4oQ1FqM",
    "Biocon Hebbagodi": "ChIJx19GElxsrjsRafNq-buRnPM",
    "Delta Electronics Bommasandra": "ChIJ69SM2khtrjsRuP3F0YoA2Go",
}


if __name__ == "__main__":
    print("BENGALURU METRO STATIONS VERIFICATION")
    print("=" * 50)

    purple_count = len(METRO_LINES['Purple Line']['stations'])
    green_count = len(METRO_LINES['Green Line']['stations'])
    yellow_count = len(METRO_LINES['Yellow Line']['stations'])
    print(f"Purple Line: {purple_count} stations")
    print(f"Green Line: {green_count} stations")
    print(f"Yellow Line: {yellow_count} stations")

    total_in_lines = purple_count + green_count + yellow_count
    real_interchanges = len(INTERCHANGE_STATIONS)
    estimated_unique = total_in_lines - real_interchanges  # each interchange counted twice in lines
    print(f"\nTotal across lines (with double-count at interchanges): {total_in_lines}")
    print(f"Unique stations estimated (subtracting real interchanges once): {estimated_unique}")

    # Coordinates coverage
    covered = sum(1 for s in ALL_STATIONS if s in STATION_COORDINATES)
    print(f"\nCoordinates available for {covered}/{len(ALL_STATIONS)} stations")
    missing = [s for s in ALL_STATIONS if s not in STATION_COORDINATES]
    if missing:
        print("Missing coordinates for:")
        for s in missing:
            print(f"- {s}")
    else:
        print("All station coordinates present.")

    print("\nInterchanges:")
    for st, lines in INTERCHANGE_STATIONS.items():
        print(f"- {st}: {lines[0]} <-> {lines[1]}")

    print("\nCHARACTERISTICS:")
    for k, v in BENGALURU_METRO_CHARACTERISTICS.items():
        print(f"- {k}: {v}")


