import pytest
import p4
import connection
import psycopg2

def test_get_cursor():
	'''
	Tests that the connection is valid and that postgis exists.
	'''
	conn, cur = p4.get_cursor()
	cur.execute("SELECT PostGIS_full_version();")
	postgis_exists = cur.fetchall()
	assert conn
	assert postgis_exists

def test_submit():
	'''
	Tests the submit function.
	'''
	conn, cur = p4.get_cursor()
	p4.submit("1600 pennsylvania ave washington dc",
			  "a test review of the white house",
			  {'x': -77.03535, 'y': 38.898754},
			  cur)
	cur.execute("""
		SELECT COUNT(*) FROM reviews
		WHERE address = '1600 pennsylvania ave washington dc'
		AND review = 'a test review of the white house'
		AND ST_x(location) = -77.03535
		AND ST_y(location) = 38.898754;
		""")
	count = cur.fetchone()[0]
	conn.rollback()
	assert count >= 1

def test_find():
	'''
	Tests the find function.
	'''
	conn, cur = p4.get_cursor()
	p4.submit("1600 pennsylvania ave washington dc",
			  "a test review of the white house",
			  {'x': -77.03535, 'y': 38.898754},
			  cur)
	search = p4.find("1600 pennsylvania ave washington dc",
					 {'x': -77.03535, 'y': 38.898754},
					 0, cur)
	conn.rollback()
	assert search
