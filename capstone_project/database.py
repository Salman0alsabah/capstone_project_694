from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, DateTime, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import select, and_

# Database configuration
db_url = 'mysql+pymysql://root:Salmlm1122@127.0.0.1/bad_links_database'

# Create a database engine
engine = create_engine(db_url)

# Define the table structure
metadata = MetaData()
bad_links = Table('bad_links_database', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('url', String(2048), unique=True, nullable=False),
                  Column('status', String(100), nullable=False),
                  Column('scan_date', DateTime, default=func.current_timestamp()))

# Function to insert a bad link into the database
def store_bad_link(url, status='bad'):
    try:
        with engine.connect() as connection:
            # Check if the URL already exists in the database
            query = select([func.count()]).select_from(bad_links).where(bad_links.c.url == url)
            result = connection.execute(query)
            count = result.scalar()

            if count == 0:
                # Insert the bad link if it doesn't exist
                insert_stmt = bad_links.insert().values(url=url, status=status)
                connection.execute(insert_stmt)
                print(f"Bad link stored: {url}")
            else:
                print("Link already exists in the database.")

    except SQLAlchemyError as e:
        print(f"Database error: {e}")

# Function to check if the URL is in the database and its status
def check_url_in_database(url):
    try:
        with engine.connect() as connection:
            query = select([bad_links.c.status]).where(bad_links.c.url == url)
            result = connection.execute(query)
            row = result.fetchone()

            if row:
                return row[0]  # Return the status of the URL
            else:
                return None  # URL not found in the database
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return None