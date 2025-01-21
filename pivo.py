import sqlite3
import csv

conn = sqlite3.connect('pivo.db')
c = conn.cursor()

# Export všech piv do CSV
c.execute("SELECT * FROM Pivo")
rows = c.fetchall()

with open('piva.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([description[0] for description in c.description])  # Zápis názvů sloupců
    writer.writerows(rows)

conn.close()
