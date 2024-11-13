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
# File Name         :       ./app/config.py
# Created By        :       Satya Prakash Nigam <spnigam25@yahoo.com>
# Created Date      :       Nov 12, 2024
# version           :       1.0
# Release           :       R1
#
# Dependencies      :       python-dotenv
#
# Installation      :       $ pip install requirements.txt
#
# Usage             :       Import Config class in application
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

# config.py
'''
    Application Configuration Settings
'''

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Base configuration class.
    
    Attributes:
        SECRET_KEY (str): Secret key for Flask application.
        MYSQL_HOST (str): MySQL host.
        MYSQL_USER (str): MySQL username.
        MYSQL_PASSWORD (str): MySQL password.
        MYSQL_DB (str): MySQL database name.
        MYSQL_SSL_MODE (str): MySQL SSL mode.
        MYSQL_CONNECT_STRING (str): MySQL connection string.
        DEBUG (bool): Flask debug mode.
        TESTING (bool): Flask testing mode.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'bookstore_db')
    MYSQL_SSL_MODE = os.environ.get('MYSQL_SSL_MODE', 'DISABLED')

    MYSQL_CONNECT_STRING = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}?ssl_mode={MYSQL_SSL_MODE}"

    # Flask settings
    DEBUG = os.environ.get('FLASK_DEBUG', False)
    TESTING = os.environ.get('FLASK_TESTING', False)


class DevelopmentConfig(Config):
    """
    Development configuration class.
    
    Attributes:
        DEBUG (bool): Flask debug mode.
    """
    DEBUG = True


class ProductionConfig(Config):
    """
    Production configuration class.
    
    Attributes:
        DEBUG (bool): Flask debug mode.
    """
    DEBUG = False 