import json
import urllib.request
from datetime import date

# url = 'https://data.boston.gov/api/3/action/datastore_search?resource_id=dc615ff7-2ff3-416a-922b-f0f334f085d0&limit=5&q=title:jones'  

url = f'https://data.boston.gov/api/3/action/datastore_search_sql?sql=SELECT%20*%20from%20%22dc615ff7-2ff3-416a-922b-f0f334f085d0%22%20WHERE%20%%22%date%22%20%22%=%22%%20%%22%2022-11-20%%22%'
# https://data.boston.gov/api/3/action/datastore_search_sql?sql=SELECT%20*%20from%20%22dc615ff7-2ff3-416a-922b-f0f334f085d0%22%20WHERE%20%%22%neighborhood%22%20%22LIKE%22%20%22Boston%22
# THIS WORKS https://data.boston.gov/api/3/action/datastore_search_sql?sql=SELECT * from "dc615ff7-2ff3-416a-922b-f0f334f085d0" where neighborhood LIKE 'Boston'

fileobj = urllib.request.urlopen(url)
response_dict = json.loads(fileobj.read())
print(response_dict)

# Execute SQL queries on the DataStore
# The datastore_search_sql action allows a user to search data in a resource
# or connect multiple resources with join expressions. The underlying SQL         
# engine is the `PostgreSQL engine <http://www.postgresql.org/docs/9.1/interactive/>`_.
# There is an enforced timeout on SQL queries to avoid an unintended DOS.
# The number of results returned is limited to 32000, unless set in the
# site's configuration ``ckan.datastore.search.rows_max``
# DataStore resource that belong to a private CKAN resource cannot be
# searched with this action. Use :meth:`~ckanext.datastore.logic.action.datastore_search` instead.
# .. note:: This action is only available when using PostgreSQL 9.X and using a read-only user on the database.    
# It is not available in :ref:`legacy mode<legacy-mode>`.
# :param sql: a single SQL select statement
# :type sql: string**Results:**
# The result of this action is a dictionary with the following keys:
    # :rtype: A dictionary with the following keys
    # :param fields: fields/columns and their extra metadata
    # :type fields: list of dictionaries
    # :param records: list of matching results
    # :type records: list of dictionaries