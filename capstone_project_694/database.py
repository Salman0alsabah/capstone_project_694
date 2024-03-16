from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, DateTime,select, func, insert
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
        with engine.begin() as connection:  # Use begin() for a transactional block
            # Check if the URL already exists in the database
            query = select(func.count()).select_from(bad_links).where(bad_links.c.url == url)
            result = connection.execute(query)
            count = result.scalar()

            if count == 0:
                # Insert the bad link if it doesn't exist
                insert_stmt = insert(bad_links).values(url=url, status=status)
                connection.execute(insert_stmt)
                print(f"Bad link stored: {url}")
            else:
                print("Link already exists in the database.")
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return  # Return to ensure we don't proceed after an error

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
    
# Function to fetch and sort links from latest to oldest
def fetch_sorted_links():
    try:
        with engine.connect() as connection:
            query = select(bad_links).order_by(bad_links.c.scan_date.desc())
            result = connection.execute(query)
            rows = result.fetchall()

            sorted_links = []
            for row in rows:
                # Assuming the order of columns in your select query is id, url, status, scan_date
                # Access columns by index
                sorted_links.append({
                    'url': row[1],  # Access the second column (url)
                    'status': row[2],  # Access the third column (status)
                    'scan_date': row[3]  # Access the fourth column (scan_date)
                })

            return sorted_links

    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return []
