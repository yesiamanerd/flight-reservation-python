# Import necessary libraries
# import the connector
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import Table, MetaData
from sqlalchemy.dialects.mysql import insert


# establish a connection to MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="educative",
    password="secret",
    database="flight"
)

# create a cusrsor object to perform quries
mycursor = connection.cursor()

# Step 1: Create a DataFrame with the data
df = pd.read_csv('../dataset/airlines.csv')

# Step 2: Create a SQLAlchemy engine to connect to the MySQL database
engine = create_engine("mysql+mysqlconnector://educative:secret@localhost/flight")


print("AIRLINES CSV DATA:")
print(df.head())
print(f"Number of rows: {len(df)}")

# Step 3: Convert the Pandas DataFrame to a format for MySQL table insertion
def upsert_airlines(df, table_name, engine):
    meta = MetaData()
    meta.reflect(bind=engine)
    table = meta.tables[table_name]

    with engine.begin() as conn:  # <-- engine.begin() instead of connect()
        for _, row in df.iterrows():
            stmt = insert(table).values(**row.to_dict())
            stmt = stmt.on_duplicate_key_update(**row.to_dict())
            conn.execute(stmt)



upsert_airlines(df, 'airline', engine)
#df.to_sql('Airline', con=engine, if_exists='append', index=False, method='multi')

connection.commit()

# print(mycursor.rowcount, "record inserted.")
# mycursor.execute("Select * from Airline")


################################################################################################################

# Load the dataframe from the CSV file
df = pd.read_csv('../dataset/airports.csv')

mycursor = connection.cursor()







# Function to insert into the Address table and get address_id
def insert_address(city, state, country):
    with connection.cursor() as cur:
        cur.execute("""
            INSERT INTO Address (city, state, country)
            VALUES (%s, %s, %s)
        """, (city, state, country))
        connection.commit()
        return cur.lastrowid


# Iterate over each row in the dataframe
for index, row in df.iterrows():
    # Extract city, state, country
    city = row['city']
    state = row['state']
    country = row['country']

    # Insert into Address and get address_id
    address_id = insert_address(city, state, country)

    # Insert into Airport using the code, name, and address_id
    with connection.cursor() as cur:
        cur.execute("""
            INSERT INTO Airport (code, name, address_id)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE name=VALUES(name), address_id=VALUES(address_id)
        """, (row['code'], row['name'], address_id))
        connection.commit()



################################################################################################################

# Load the dataframe from the CSV file
flights_df = pd.read_csv('../dataset/flights.csv')
# print(flights_df.columns)
# Create a cursor object
mycursor = connection.cursor()

# Prepare an SQL query to insert data into the Flight table
# flight_no
insert_flight_query = """
                      INSERT INTO Flight (airline_code, distance_km, dep_time, arri_time, dep_port, arri_port, \
                                          booked_seats)
                      VALUES (%s, %s, %s, %s, %s, %s, 0) \
                      """

# Select only the relevant columns
relevant_columns = ['airline_code', 'distance_km', 'dep_time', 'arri_time', 'dep_port', 'arri_port']

# Convert the selected columns to tuples (rows of data)
flight_data = [tuple(row) for row in flights_df[relevant_columns].values]

# Execute the insert query for each row of flight data
batch_size = 1000  # Adjust the batch size as needed

for i in range(0, len(flight_data), batch_size):
    batch = flight_data[i:i + batch_size]
    with connection.cursor() as cur:
        cur.executemany(insert_flight_query, batch)
        connection.commit()

print(f"{len(flight_data)} flights inserted into the database.")

################################################################################################################


with connection.cursor() as cur:
    cur.execute("INSERT INTO Role(name) VALUES ('admin') ON DUPLICATE KEY UPDATE name='admin';")
    cur.execute("INSERT INTO Role(name) VALUES ('user') ON DUPLICATE KEY UPDATE name='user';")

    cur.execute("""
        INSERT INTO Account(username, password, status)
        VALUES ('admin_user', '12345', 'active')
        ON DUPLICATE KEY UPDATE password='12345', status='active';
    """)

    cur.execute("SELECT account_id FROM Account WHERE username = 'admin_user';")
    admin_account_id = cur.fetchone()[0]

    cur.execute("SELECT role_id FROM Role WHERE name = 'admin';")
    admin_role_id = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO Account_Role(account_id, role_id)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE account_id=account_id;
    """, (admin_account_id, admin_role_id))

    connection.commit()

mycursor.close()
connection.close()