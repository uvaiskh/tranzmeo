import pandas as pd
import geopy.distance
import pyodbc

df_lat_long = pd.read_csv('csv_files/latitude_longitude_details.csv', encoding='utf-8')


def connect_to_db():
    server = 'UVAIS\SQLEXPRESS'
    database = 'TEST'
    username = 'uvais'
    password = 'testPassword'
    client = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    return client


def find_out_of_line_coordinates(data_frame):
    x0 = data_frame['latitude'][0]
    y0 = data_frame['longitude'][0]
    x1 = data_frame['latitude'][1]
    y1 = data_frame['longitude'][1]
    out_items = list()
    for i in range(2, len(data_frame)):
        x, y = data_frame['latitude'][i], data_frame['longitude'][i]
        if round((x0 - x1) * (y1 - y), 5) != round((x1 - x) * (y0 - y1), 5):
            out_items.append((x, y))
    return out_items


def find_distance_between_coordinates(c1, c2):
    dist = geopy.distance.geodesic(c1, c2)
    return dist.kilometers


def match_coordinates_with_terrain(data_frame_ll):
    try:
        c1 = (data_frame_ll['latitude'][0], data_frame_ll['longitude'][0])
        client = connect_to_db()
        rows = list()
        for index, row in data_frame_ll.iterrows():
            c2 = (row['latitude'], row['longitude'])
            dist = geopy.distance.geodesic(c1, c2)
            kms = dist.kilometers
            if kms <= 0:
                rows.append(((row['latitude'], row['longitude']), 'boundary wall'))
                rows.append(((row['latitude'], row['longitude']), 'road'))
            elif 0 < kms <= 0.5:
                rows.append(((row['latitude'], row['longitude']), 'road'))
            elif 0.5 < kms <= 1.5:
                rows.append(((row['latitude'], row['longitude']), 'river side'))
            elif 1.5 < kms <= 3:
                rows.append(((row['latitude'], row['longitude']), 'civil station'))
                rows.append(((row['latitude'], row['longitude']), 'road'))
        values = ', '.join(map(str, rows))
        query = "INSERT INTO co_terrain (coordinate,terrain) values {}".format(values)
        cursor = client.cursor()
        cursor.execute(query)
        client.commit()
        return None
    except Exception as err:
        return str(err)


items = find_out_of_line_coordinates(df_lat_long)
print("Coordinates that are out of line: ", items)

err = match_coordinates_with_terrain(df_lat_long)
if err:
    print("Failed to add data", err)

client = connect_to_db()
cursor = client.cursor()
cursor.execute("SELECT coordinate FROM co_terrain where terrain='road' AND coordinates NOT IN "
               "(SELECT  DISTINCT coordinates FROM co_terrain where terrain='civil station')")

print("Coordinates only in terrain road are: ")
for row in cursor:
    print(row)


