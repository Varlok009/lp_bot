import csv


def get_cities_for_game(path):
    cities = set()
    with open(path, 'r', encoding='utf-8') as f:
        fields = ["city_name", "region"]
        reader = csv.DictReader(f, fields, delimiter=';')
        for row in reader:
            if row["city_name"] and 'Оспаривается' not in row["city_name"]:
                cities.add(row["city_name"].lower())
    return cities
