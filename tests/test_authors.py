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
# File Name         :       ./tests/test_authors.py
# Created By        :       Satya Prakash Nigam <spnigam25@yahoo.com>
# Created Date      :       Nov 12, 2024
# version           :       1.0
# Release           :       R1
#
# Dependencies      :       pytest, Flask
#
# Installation      :       $ pip install requirements.txt
#
# Usage             :       Run tests using : pytest tests/
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

# test_authors.py
'''
    Test Suite for Authors API Endpoints
    ======================================

    This test suite covers all authors API endpoints:
        - GET /authors
        - GET /authors/:id
        - POST /authors
        - PUT /authors/:id
        - DELETE /authors/:id
        - PATCH /authors/:id/restore

    Run these tests using pytest tests/ to ensure your API is working correctly.
'''
"""
# ---------------------------------------------------------------------------
# Running Tests and Viewing Coverage Report
# -----------------------------------------
#
# To run tests and generate an HTML coverage report, execute:
#   pytest --cov=app --cov-report=html tests/
#
# To view the HTML report, navigate to the generated htmlcov/ directory and open index.html:
#   cd htmlcov/
#   start index.html (on Windows) or open index.html (on Mac/Linux)
#
# Note: Exclude the htmlcov/ directory from Git commits by adding it to .gitignore.
"""

import pytest
from app import app
from app.database import db
import uuid

@pytest.fixture
def client():
    """
    Pytest fixture to create a test client.

    Returns:
        client (FlaskClient): Test client instance.
    """
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


def test_get_authors(client):
    """
    Test GET /authors endpoint.

    Returns:
        200 OK
    """
    response = client.get('/authors')
    assert response.status_code == 200


def test_get_author_by_id(client):
    """
    Test GET /authors/:id endpoint.

    Returns:
        200 OK
    """
    # Create an author for testing
    data = {'name': 'Test Author', 'email': 'test@author.com'}
    client.post('/authors', json=data)

    response = client.get('/authors/1')
    assert response.status_code == 200


def test_get_non_existent_author(client):
    """
    Test GET /authors/:id endpoint with non-existent ID.

    Returns:
        404 NOT FOUND
    """
    response = client.get('/authors/999')
    assert response.status_code == 404


def test_create_author(client):
    """
    Test POST /authors endpoint.

    Returns:
        201 CREATED
    """
    unique_email = f"new-{uuid.uuid4()}@author.com"
    data = {'name': 'New Author', 'email': unique_email}
    response = client.post('/authors', json=data)
    assert response.status_code == 201


def test_create_author_missing_fields(client):
    """
    Test POST /authors endpoint with missing fields.

    Returns:
        400 BAD REQUEST
    """
    data = {'name': 'New Author'}
    response = client.post('/authors', json=data)
    assert response.status_code == 400
    
#######################################################
 
def test_update_author(client):
    """
    Test PUT /authors/:id endpoint.

    Returns:
        200 OK

    Scenario:
        - Create an author
        - Update the author's details
    """
    # Create an author for testing
    data = {'name': 'Test Author', 'email': 'test@author.com'}
    client.post('/authors', json=data)

    updated_data = {'name': 'Updated Author', 'email': 'updated@author.com'}
    response = client.put('/authors/1', json=updated_data)
    assert response.status_code == 200


def test_update_non_existent_author(client):
    """
    Test PUT /authors/:id endpoint with non-existent ID.

    Returns:
        404 NOT FOUND

    Scenario:
        - Attempt to update an author that does not exist
    """
    updated_data = {'name': 'Updated Author', 'email': 'updated@author.com'}
    response = client.put('/authors/999', json=updated_data)
    assert response.status_code == 404


def test_delete_author(client):
    """
    Test DELETE /authors/:id endpoint.

    Returns:
        200 OK

    Scenario:
        - Create an author
        - Soft delete the author
    """
    # Create an author for testing
    data = {'name': 'Test Author', 'email': 'test@author.com'}
    client.post('/authors', json=data)

    response = client.delete('/authors/1')
    assert response.status_code == 200


def test_delete_non_existent_author(client):
    """
    Test DELETE /authors/:id endpoint with non-existent ID.

    Returns:
        404 NOT FOUND

    Scenario:
        - Attempt to delete an author that does not exist
    """
    response = client.delete('/authors/999')
    assert response.status_code == 404


def test_restore_author(client):
    """
    Test PATCH /authors/:id/restore endpoint.

    Returns:
        200 OK

    Scenario:
        - Create an author
        - Soft delete the author
        - Restore the author
    """
    # Create an author for testing
    data = {'name': 'Test Author', 'email': 'test@author.com'}
    client.post('/authors', json=data)

    # Soft delete the author
    client.delete('/authors/1')

    response = client.patch('/authors/1/restore')
    assert response.status_code == 200


def test_restore_non_existent_author(client):
    """
    Test PATCH /authors/:id/restore endpoint with non-existent ID.

    Returns:
        404 NOT FOUND

    Scenario:
        - Attempt to restore an author that does not exist
    """
    response = client.patch('/authors/999/restore')
    assert response.status_code == 404


def test_restore_already_active_author(client):
    """
    Test PATCH /authors/:id/restore endpoint with already active author.

    Returns:
        400 BAD REQUEST

    Scenario:
        - Create an author
        - Attempt to restore the author without deleting it first
    """
    # Create an author for testing
    data = {'name': 'Test Author', 'email': 'test@author.com'}
    client.post('/authors', json=data)

    response = client.patch('/authors/1/restore')
    assert response.status_code == 400

