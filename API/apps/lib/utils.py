def calculate_konversi(value: dict, data_konversi: list) -> dict:
    konversi = {
        "pieces": 0,
        "box": 0,
        "karton": 0
    }

    level1 = next((val for val in data_konversi if val["level"] == 1), None)
    level2 = next((val for val in data_konversi if val["level"] == 2), None)
    level3 = next((val for val in data_konversi if val["level"] == 3), None)

    if not (level2 and level3):
        raise ValueError("Level 2 and Level 3 konversi data is required.")

    konversi["pieces"] = (
            value.get("pieces", 0)
            + value.get("box", 0) * level2["faktor_konversi"]
            + value.get("karton", 0) * level3["faktor_konversi"]
    )

    konversi["box"] = konversi["pieces"] // level2["faktor_konversi"]
    konversi["karton"] = konversi["pieces"] // level3["faktor_konversi"]

    return konversi
