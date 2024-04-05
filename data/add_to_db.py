import mysql.connector
import json

# Create a connection to the database
cnx = mysql.connector.connect(user='root', password='CHANGE_ME',
                              host='localhost',
                              database='projet_humanite')

# Create a cursor object
cursor = cnx.cursor()
cursor.execute("ALTER TABLE communes AUTO_INCREMENT = 0;")

# Insert the data into the database
with open('./data/communes.json', 'r') as f:
    communes = json.load(f)

for commune in communes:
    add_commune = ("INSERT INTO communes "
                   "(nom, url, lat, lon) "
                   "VALUES (%s, %s, %s, %s)")
    data_commune = (commune['nom'], commune['url'],
                    commune['lat'], commune['lon'])
    cursor.execute(add_commune, data_commune)

# Insert the data into the database
with open('./data/fusions_data.json', 'r') as f:
    final_fusion_data = json.load(f)

for data in final_fusion_data:
    # Get the ID for the 'Nom de la nouvelle commune' from the 'communes' table
    cursor.execute("SELECT id FROM communes WHERE nom = %s",
                   (data['Nom de la nouvelle commune'],))
    id_nouv_com = cursor.fetchone()[0]

    # For each commune in 'Communes reunies', get the ID from the 'communes' table and insert it into the 'fusions' table
    for commune in data['Communes reunies']:
        cursor.execute("SELECT id FROM communes WHERE nom = %s", (commune,))
        id_reuni_com = cursor.fetchone()[0]

        cursor.execute("INSERT INTO fusions (id_nouv_com, id_reuni_com, date) VALUES (%s, %s, %s)",
                       (id_nouv_com, id_reuni_com, data['Date']))

# Insert the creation data into the database
with open('./data/creations_data.json', 'r') as f:
    creation_data = json.load(f)

for data in creation_data:
    # For each commune in 'Nom de la commune creee', get the ID from the 'communes' table
    for commune in data['Nom de la commune creee']:
        cursor.execute("SELECT id FROM communes WHERE nom = %s", (commune,))
        id_com_cree = cursor.fetchone()[0]

        # Get the ID for the 'Commune affectee' from the 'communes' table
        cursor.execute("SELECT id FROM communes WHERE nom = %s",
                       (data['Commune affectee'],))
        id_com_affectee = cursor.fetchone()[0]

        cursor.execute("INSERT INTO creations (id_com_cree, id_com_affectee, mode, date) VALUES (%s, %s, %s, %s)",
                       (id_com_cree, id_com_affectee, data['Mode de creation'], data['Date']))


# Insert the modification data into the database
with open('./data/modifications_data.json', 'r') as f:
    modification_data = json.load(f)

for data in modification_data:
    # Get the ID for the 'Ancien nom' from the 'communes' table
    cursor.execute("SELECT id FROM communes WHERE nom = %s", (data['Ancien nom'],))
    result = cursor.fetchone()
    if result is not None:
        id_ancien = result[0]
    else:
        print(f"Commune {data['Ancien nom']} not found in 'communes' table.")
        continue

    # Get the ID for the 'Nouveau nom' from the 'communes' table
    cursor.execute("SELECT id FROM communes WHERE nom = %s", (data['Nouveau nom'],))
    result = cursor.fetchone()
    if result is not None:
        id_nouveau = result[0]
    else:
        print(f"Commune {data['Nouveau nom']} not found in 'communes' table.")
        continue

    cursor.execute("INSERT INTO modifications (id_ancien, id_nouveau, date) VALUES (%s, %s, %s)",
                   (id_ancien, id_nouveau, data['Date']))


# Commit the changes
cnx.commit()

# Close the cursor and connection
cursor.close()
cnx.close()
