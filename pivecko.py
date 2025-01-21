import sqlite3
import folium

conn = sqlite3.connect("pivo.db")
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS Pivo (
    ID_Piva INTEGER PRIMARY KEY AUTOINCREMENT,
    Nazev TEXT NOT NULL,
    Typ TEXT,
    Obsah_Alkoholu REAL,
    ID_Vyrobce INTEGER,
    FOREIGN KEY (ID_Vyrobce) REFERENCES Vyrobce(ID_Vyrobce)
)''')

c.execute('''CREATE TABLE IF NOT EXISTS Mesto (
    ID_Mesta INTEGER PRIMARY KEY AUTOINCREMENT,
    Nazev TEXT NOT NULL,
    GPS_Latitude REAL,
    GPS_Longitude REAL,
    Zeme TEXT NOT NULL
)''')

c.execute('''CREATE TABLE IF NOT EXISTS Vyrobce (
    ID_Vyrobce INTEGER PRIMARY KEY AUTOINCREMENT,
    Nazev TEXT NOT NULL,
    Rok_Zalozeni INTEGER,
    ID_Mesta INTEGER,
    FOREIGN KEY (ID_Mesta) REFERENCES Mesto(ID_Mesta)
)''')

def insert_all_data():
    mesta = [
        ("Praha", 50.0755, 14.4378, "Česká republika"),
        ("Plzeň", 49.7384, 13.3736, "Česká republika"),
        ("Brno", 49.1951, 16.6068, "Česká republika"),
        ("Ostrava", 49.8340, 18.2923, "Česká republika"),
        ("Liberec", 50.7671, 15.0562, "Česká republika"),
        ("Berlín", 52.5200, 13.4050, "Německo"),
        ("Mnichov", 48.1351, 11.5820, "Německo"),
        ("Kolín nad Rýnem", 50.9375, 6.9603, "Německo"),
        ("Brusel", 50.8503, 4.3517, "Belgie"),
        ("Antverpy", 51.2194, 4.4025, "Belgie"),
        ("Gent", 51.0543, 3.7174, "Belgie"),
        ("New York", 40.7128, -74.0060, "USA"),
        ("Chicago", 41.8781, -87.6298, "USA"),
        ("Los Angeles", 34.0522, -118.2437, "USA"),
        ("Tokio", 35.6895, 139.6917, "Japonsko"),
        ("Osaka", 34.6937, 135.5023, "Japonsko"),
        ("Sapporo", 43.0618, 141.3545, "Japonsko"),
        ("Buenos Aires", -34.6037, -58.3816, "Argentina"),
        ("Córdoba", -31.4201, -64.1888, "Argentina"),
        ("Mendoza", -32.8908, -68.8272, "Argentina")
    ]
    c.executemany('INSERT INTO Mesto (Nazev, GPS_Latitude, GPS_Longitude, Zeme) VALUES (?, ?, ?, ?)', mesta)

    vyrobci = [
        ("Pilsner Urquell", 1842, 2),
        ("Staropramen", 1869, 1),
        ("Starobrno", 1872, 3),
        ("Ostravar", 1897, 4),
        ("Svijany", 1564, 5),
        ("Berliner Kindl", 1872, 6),
        ("Hofbräu München", 1589, 7),
        ("Gaffel Kölsch", 1908, 8),
        ("Brasserie Cantillon", 1900, 9),
        ("De Koninck", 1833, 10),
        ("Gruut Brewery", 2009, 11),
        ("Brooklyn Brewery", 1988, 12),
        ("Goose Island", 1988, 13),
        ("Angel City Brewery", 2010, 14),
        ("Sapporo", 1876, 17),
        ("Asahi", 1889, 16),
        ("Kirin", 1885, 15),
        ("Quilmes", 1888, 18),
        ("Patagonia", 2006, 19),
        ("Andes", 1921, 20)
    ]
    c.executemany('INSERT INTO Vyrobce (Nazev, Rok_Zalozeni, ID_Mesta) VALUES (?, ?, ?)', vyrobci)

    piva = [
        ("Pilsner", "Ležák", 4.4, 1),
        ("Staropramen", "Ležák", 5.0, 2),
        ("Starobrno Medium", "Ležák", 4.7, 3),
        ("Ostravar Premium", "Ležák", 5.1, 4),
        ("Svijanský Rytíř", "Ležák", 5.0, 5),
        ("Velkopopovický Kozel", "Ležák", 4.8, 6),
        ("Gambrinus Premium", "Ležák", 4.5, 7),
        ("Brněnský ležák", "Ležák", 5.0, 8),
        ("Ostravar Premium", "Ležák", 5.2, 9),
        ("Svijanský Máz", "Ležák", 5.1, 10),
        ("Berliner Weisse", "Pšeničné", 3.0, 11),
        ("Hofbräu Original", "Ležák", 5.1, 12),
        ("Gaffel Kölsch", "Kolsch", 4.8, 13),
        ("Cantillon Gueuze", "Lambic", 5.0, 14),
        ("De Koninck", "Amber Ale", 5.2, 15),
        ("Gruut Blonde", "Blonde Ale", 5.5, 16),
        ("Brooklyn Lager", "Ležák", 5.2, 17),
        ("312 Urban Wheat Ale", "Pšeničné", 4.2, 18),
        ("Angel City IPA", "IPA", 6.1, 19),
        ("Sapporo Premium", "Ležák", 5.0, 20),
        ("Asahi Super Dry", "Ležák", 5.0, 21),
        ("Kirin Ichiban", "Ležák", 5.0, 22),
        ("Quilmes Cristal", "Ležák", 4.9, 23),
        ("Patagonia Amber Lager", "Ležák", 5.5, 24),
        ("Andes Roja", "Červené", 6.0, 25)
    ]
    c.executemany('INSERT INTO Pivo (Nazev, Typ, Obsah_Alkoholu, ID_Vyrobce) VALUES (?, ?, ?, ?)', piva)

    conn.commit()

insert_all_data()

def create_map():
    c.execute('''SELECT Mesto.Nazev, Mesto.GPS_Latitude, Mesto.GPS_Longitude, Vyrobce.Nazev 
                 FROM Mesto 
                 JOIN Vyrobce ON Mesto.ID_Mesta = Vyrobce.ID_Mesta''')
    data = c.fetchall()

    mapa = folium.Map(location=[50.0755, 14.4378], zoom_start=2)

    for mesto, lat, lon, vyrobce in data:
        folium.Marker(
            location=[lat, lon],
            popup=f"{vyrobce} ({mesto})",
            tooltip=vyrobce
        ).add_to(mapa)

    mapa.save("pivovary_map.html")

create_map()

conn.close()
