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
# File Name         :       ./app/database.py
# Created By        :       Satya Prakash Nigam <spnigam25@yahoo.com>
# Created Date      :       Nov 12, 2024
# version           :       1.0
# Release           :       R1
#
# Dependencies      :       mysql-connector-python
#
# Installation      :       $ pip install requirements.txt
#
# Usage             :       Import db object in application
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

# database.py
'''
    MySQL Database Connection Module
    ===============================
'''

import mysql.connector
from . import config
 
def get_database_config():
    """
    Returns MySQL database configuration.

    Returns:
        dict: Database configuration
    """
    return {
        'host': config.Config.MYSQL_HOST,
        'user': config.Config.MYSQL_USER,
        'password': config.Config.MYSQL_PASSWORD,
        'database': config.Config.MYSQL_DB,
        'ssl_disabled': True
    }


mysql_config = get_database_config()


def establish_database_connection():
    """
    Establishes a connection to the MySQL database.

    Returns:
        mysql.connector.connection.MySQLConnection: Database connection object
    """
    return mysql.connector.connect(**mysql_config)


db = establish_database_connection() 