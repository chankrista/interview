"""Business Reviewer
Submit a review for a business based on address and look up reviews
based on distance from an address.

Usage:
  p4.py submit <address> <review> 
  p4.py find <address> --m=<miles>
  p4.py (-h | --help)
  p4.py (-v | --version)

Options:
  submit           Submits a review.
  find             Looks up reviews based on distance from an address.
  <review>         The text of the review.
  <address>        The address of the business to submit a review for or
                   from which to look up reviews.
  --m=<miles>      The radius in miles from the location entered to conduct
                   the search of reviews.
  -h --help        Show this screen.

Examples:

  Submit the review "better than shake shack!" for business at "50 Ranch Dr, Milpitas, CA":
  $ p4.py submit "50 Ranch Dr, Milpitas, CA" "better than shake shack!"

  Look up reviews of businesses within 1 mile of "1847 columbia rd nw washington dc 20009":
  $ p4.py find "1847 columbia rd nw washington dc 20009" --m=1

"""

from docopt import docopt
import psycopg2
import censusgeocode as cg
from prettytable import PrettyTable
import connection

def get_cursor():
    '''
    Creates the database 'restaurant_reviews' if it does not exist and adds a
    postgis extension if it does not exist. Changes the connection to the
    database 'restaurant_reviews' and returns the connection and cursor.
    '''
    conn = psycopg2.connect(
        host=connection.HOST,
        user=connection.USER,
        password=connection.PASSWORD)
    cur = conn.cursor()

    # Check if database restaurant_reviews exists. If not, create it.
    cur.execute(
        "SELECT 1 FROM pg_catalog.pg_database \
        WHERE datname = 'restaurant_reviews'")
    exists = cur.fetchone()
    if not exists:
        cur.execute('CREATE DATABASE restaurant_reviews')

    # If not currently connected to restaurant_reviews, reconnect to it.
    cur.execute("SELECT current_database();")
    current_db = cur.fetchone()[0]
    if current_db != 'restaurant_reviews':
        conn = psycopg2.connect(
        dbname='restaurant_reviews',
        host=connection.HOST,
        user=connection.USER,
        password=connection.PASSWORD)
        cur = conn.cursor()
    cur.execute('CREATE EXTENSION IF NOT EXISTS postgis;')  
    return conn, cur


def submit(address, review, coordinates, cur):
    '''
    Given an address, review, dictionary of coordinates (with 'x' and 'y' as
    keys representing longitude and latitude, respectively), and a cursor,
    inserts the address, review, and coordinates as a point into the 'reviews'
    table.
    '''
    cur.execute(
        """CREATE TABLE IF NOT EXISTS reviews 
        (address text, review text, location GEOMETRY);
        """)

    cur.execute("""
     INSERT INTO reviews (address, review, location)
     VALUES (%s, %s, ST_MakePoint(%s, %s));
     """,
     (address, review, coordinates['x'], coordinates['y']))


def find(address, coordinates, radius, cur):
    '''
    Given an address, a dictionary of coordinates with keys 'x' and 'y' for 
    longitude and latitude, respectively, a radius in miles, and a cursor, 
    prints the addresses, reviews, and distances that are within the given 
    radius of the location, sorted by distance.
    '''   

    cur.execute("""
    SELECT EXISTS(
    SELECT 1
    FROM   information_schema.tables 
    WHERE table_name = 'reviews');
    """)
    reviews_exists = cur.fetchone()[0]

    if reviews_exists:
        cur.execute(
            """
            SELECT address, review, ST_Distance_Sphere(
                location, ST_MakePoint(%s, %s)) / 1609.344 AS distance
            FROM reviews
            WHERE ST_Distance_Sphere(
                location, ST_MakePoint(%s, %s)) / 1609.344 <= %s
            ORDER BY distance ASC;
            """,
            (coordinates['x'], coordinates['y'], 
            coordinates['x'], coordinates['y'], radius))
        output = cur.fetchall()
        table = PrettyTable()
        if output:
            table.field_names = ["Address", "Review", "Distance (miles)"]
            for address, review, distance in output:
                table.add_row([address, review, round(distance, 2)])
            print(table)
            return True
        else:
            print("No reviews found within %s miles of %s" % (radius, address))
            return False
    else:
        print("No reviews have been submitted!")
        return False

def main():

    arguments = docopt(__doc__)   
    conn, cur = get_cursor()

    try:
        coordinates = cg.onelineaddress(
            arguments['<address>'])[0]['coordinates']
    except IndexError:
        print()
        print("Address \"%s\" could not be found!" % arguments['<address>'])
        print()
        return

    if arguments['submit']:        
        submit(arguments['<address>'], arguments['<review>'], coordinates, cur)

    if arguments['find']:
        find(arguments['<address>'], coordinates, int(arguments['--m']), cur)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    main()
