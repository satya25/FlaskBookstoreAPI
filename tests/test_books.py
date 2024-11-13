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
# File Name         :       ./tests/test_books.py
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
 
# tests/test_books.py
'''
    Test Suite for Books API Endpoints
    ======================================

    This test suite covers all books API endpoints:
        - GET /books
        - GET /books/:id
        - POST /books
        - PUT /books/:id
        - DELETE /books/:id
        - PATCH /books/:id/restore

    Run these tests using pytest tests/ to ensure your API is working correctly.
'''

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


def test_get_books(client):
    """
    Test GET /books endpoint.

    Returns:
        200 OK
    """
    response = client.get('/books')
    assert response.status_code == 200


def test_get_book_by_id(client):
    """
    Test GET /books/:id endpoint.

    Returns:
        200 OK
    """
    # Create a book for testing
    data = {'title': 'Test Book', 'author_id': 1, 'publication_date': '2022-01-01'}
    client.post('/books', json=data)

    response = client.get('/books/1')
    assert response.status_code == 200


def test_get_non_existent_book(client):
    """
    Test GET /books/:id endpoint with non-existent ID.

    Returns:
        404 NOT FOUND
    """
    response = client.get('/books/999')
    assert response.status_code == 404


def test_create_book(client):
    """
    Test POST /books endpoint.

    Returns:
        201 CREATED
    """
    unique_title = f"New-{uuid.uuid4()}-Book"
    data = {'title': unique_title, 'author_id': 1, 'publication_date': '2022-01-01'}
    response = client.post('/books', json=data)
    assert response.status_code == 201


def test_create_book_missing_fields(client):
    """
    Test POST /books endpoint with missing fields.

    Returns:
        400 BAD REQUEST
    """
    data = {'title': 'New Book'}
    response = client.post('/books', json=data)
    assert response.status_code == 400


def test_update_book(client):
    """
    Test PUT /books/:id endpoint.

    Returns:
        200 OK

    Scenario:
        - Create a book
        - Update the book's details
    """
    # Create a book for testing
    data = {'title': 'Test Book', 'author_id': 1, 'publication_date': '2022-01-01'}
    client.post('/books', json=data)

    updated_data = {'title': 'Updated Book', 'author_id': 1, 'publication_date': '2022-01-01'}
    response = client.put('/books/1', json=updated_data)
    assert response.status_code == 200


def test_update_non_existent_book(client):
    """
    Test PUT /books/:id endpoint with non-existent ID.

    Returns:
        404 NOT FOUND

    Scenario:
        - Attempt to update a book that does not exist
    """
    updated_data = {'title': 'Updated Book', 'author_id': 1, 'publication_date': '2022-01-01'}
    response = client.put('/books/999', json=updated_data)
    assert response.status_code == 404


def test_delete_book(client):
    """
    Test DELETE /books/:id endpoint.

    Returns:
        200 OK

    Scenario:
        - Create a book
        - Soft delete the book
    """
    # Create a book for testing
    data = {'title': 'Test Book', 'author_id': 1, 'publication_date': '2022-01-01'}
    client.post('/books', json=data)

    response = client.delete('/books/1')
    assert response.status_code == 200


def test_delete_non_existent_book(client):
    """
    Test DELETE /books/:id endpoint with non-existent ID.

    Returns:
        404 NOT FOUND

    Scenario:
        - Attempt to delete a book that does not exist
    """
    response = client.delete('/books/999')
    assert response.status_code == 404

 
def test_restore_book(client):
    """
    Test PATCH /books/:id/restore endpoint.

    Returns:
        200 OK

    Scenario:
        - Create a book
        - Soft delete the book
        - Restore the book
    """
    # Create a book for testing
    data = {'title': 'Test Book', 'author_id': 1, 'publication_date': '2022-01-01'}
    client.post('/books', json=data)

    # Soft delete the book
    client.delete('/books/1')

    response = client.patch('/books/1/restore')
    assert response.status_code == 200


def test_restore_non_existent_book(client):
    """
    Test PATCH /books/:id/restore endpoint with non-existent ID.

    Returns:
        404 NOT FOUND

    Scenario:
        - Attempt to restore a book that does not exist
    """
    response = client.patch('/books/999/restore')
    assert response.status_code == 404


def test_restore_already_active_book(client):
    """
    Test PATCH /books/:id/restore endpoint with already active book.

    Returns:
        400 BAD REQUEST

    Scenario:
        - Create a book
        - Attempt to restore the book without deleting it first
    """
    # Create a book for testing
    data = {'title': 'Test Book', 'author_id': 1, 'publication_date': '2022-01-01'}
    client.post('/books', json=data)

    response = client.patch('/books/1/restore')
    assert response.status_code == 400
    