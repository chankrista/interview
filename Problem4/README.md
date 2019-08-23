# Problem 4: Business Reviewer

Files in this folder answer problem 4:

The user wishes to submit “reviews” consisting of a location/business name and a text body tied to a location which may be either a plaintext address or a geographic point described by a latitude and longitude pair (whatever projection you prefer). If the “review” is submitted using an address, geocode this address to a point. Persist these “reviews” and allow the user to submit a bounding which for which to return/display all current “reviews” which fall within this bounding box. Your solution should be able to return results in a timely manner even when querying thousands of reviews.

## Requirements

Python 3.x
A Postgres installation with PostGIS extension
Packages documented within requirements.txt or downloaded via `pip install -r requirements.txt`
Connection details filled out and saved in connection.py

## Usage

My solution provides a command-line interface for submitting reviews to an address and finding reviews based on distance from an address. Reviews are persisted in a relation called "reviews" within a postgres database called "restaurant_reviews".

To submit a review, enter

	$ python p4.py submit <address> <review>

For example, to submit the review "better than shake shack!" for business at "50 Ranch Dr, Milpitas, CA", enter:
	$ python p4.py submit "50 Ranch Dr, Milpitas, CA" "better than shake shack!"

To look up reviews, enter

	$ python p4.py find <address> --m=<miles>

For example, to look up reviews of businesses within 1 mile of "1847 columbia rd nw washington dc 20009":
	$ python p4.py find "1847 columbia rd nw washington dc 20009" --m=1

## Tests

Test code is available within tests.py. Run using `pytest tests.py`.