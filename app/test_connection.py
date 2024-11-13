#!/usr/bin/env
# -*- coding: utf-8 -*-

"""
    This file is part of aialchemyhub_in
    (https://github.com/satya25/aialchemyhub_in).

    aialchemyhub_in is free software repository:
    You can redistribute it and/or modify it under
    the terms of the MIT License.

    aialchemyhub_in is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    MIT License for more details.

    You should have received a copy of the MIT License along with
    aialchemyhub_in.  If not, see <https://opensource.org/licenses/MIT>.
"""

# ----------------------------------------------------------------------------
# File Name         :       ./test_connection.py
# Created By        :       Satya Prakash Nigam <spnigam25@yahoo.com>
# Created Date      :       Nov 12, 2024
# version           :       1.0
# Release           :       R1
#
# Dependencies      :       Flask, mysql-connector-python
#
# Installation      :       $ pip install requirements.txt
#
# Usage             :       python test_connection.py
#
# ---------------------------------------------------------------------------
#
# Credits and Acknowledgements
#
# - Special thanks to the Python community for their excellent library:
#   https://www.python.org/community/
#
# - The APIs used in this script is documented here:
#   
#
# - Code Snippet(s) adapted from    :   -- NOT Applicable --
#
# - Dataset(s) sourced  from        :   -- NOT Applicable --
#
#
# - Inspiration for xxx drawn from:
#   
#
# Thank you to the creators and maintainers of these resources!
#
# ---------------------------------------------------------------------------
#
# - Content Removal Requests
#
#   If you are the owner or creator of any content used in this script and
#   would like it to be removed, please contact me at:  spnigam25@yahoo.com
#   I will promptly remove the content upon request.
#
# ---------------------------------------------------------------------------

# Test Connection Script
'''
    Test API Endpoint: /test-connection
        Returns all authors from the database.
'''

from app import app
from app.database import db
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a route to test database connection
@app.route('/test-connection')
def test_connection():
    """
    Test database connection by fetching all authors.

    Returns:
        dict: {'data': authors_data}
    """
    try:
        # Create a cursor object to execute SQL queries
        cursor = db.cursor()
        
        # Execute SELECT query to fetch all authors
        cursor.execute("SELECT * FROM authors")
        
        # Fetch all rows from the query result
        data = cursor.fetchall()
        
        # Close the cursor object
        cursor.close()
        
        # Log successful database connection
        logger.info('Database connection successful')
        
        # Return the fetched data as JSON
        return {'data': data}
    
    except Exception as e:
        # Log database connection error
        logger.error(f'Database connection failed: {str(e)}')
        
        # Return error response
        return {'error': 'Database connection failed'}, 500

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
 