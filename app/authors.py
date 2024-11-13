#!/usr/bin/en
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
# File Name         :       ./app/authors.py
# Created By        :       Satya Prakash Nigam <spnigam25@yahoo.com>
# Created Date      :       Nov 12, 2024
# version           :       1.0
# Release           :       R1
#
# Dependencies      :       Flask, mysql-connector-python, flasgger et al
#
# Installation      :       $ pip install requirements.txt
#
# Usage             :       python ../run.py
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

# authors.py
'''
    API Endpoints Summary
        POST /authors - Create author
        GET /authors - Get all authors
        GET /authors/:id - Get author by ID
        PUT /authors/:id - Update author
        DELETE /authors/:id - Soft-delete author
        PATCH /authors/:id/restore - Restore soft-deleted author
'''
 
from flask import Blueprint, jsonify, request
from .database import db  
import logging

authors_blueprint = Blueprint('authors', __name__)
logger = logging.getLogger(__name__)

# endpoint: GET /authors
@authors_blueprint.route('/authors', methods=['GET'])
def get_authors() -> dict:
    """
    Retrieve a list of authors.

    Returns:
        dict: A dictionary containing a list of authors.

    API Response:
        200 OK - List of authors retrieved successfully.
        500 Internal Server Error - Database error occurred.

    Response Schema:
        {
            "authors": [
                {
                    "id": int,
                    "name": str,
                    "email": str
                }
            ]
        }
    """
    try:
        cursor = db.cursor()
        query = "SELECT * FROM authors WHERE is_deleted = 0"
        cursor.execute(query)
        authors = cursor.fetchall()
        cursor.close()
        return jsonify({'authors': authors})
    except Exception as e:
        logger.error(f"Error fetching authors: {str(e)}")
        return jsonify({'error': 'Database error'}), 500


# New route: GET /authors/:id
@authors_blueprint.route('/authors/<int:author_id>', methods=['GET'])
def get_author(author_id: int) -> dict:
    """
    Retrieves an author by ID.

    Args:
        author_id (int): Author's ID.

    Returns:
        dict: JSON response with author details or error.
    """
    try:
        cursor = db.cursor()
        query = "SELECT * FROM authors WHERE id = %s AND is_deleted = 0"
        cursor.execute(query, (author_id,))
        author = cursor.fetchone()
        cursor.close()
        if author:
            return jsonify({'author': author})
        else:
            return jsonify({'error': 'Author not found'}), 404
    except Exception as e:
        logger.error(f"Error fetching author {author_id}: {str(e)}")
        return jsonify({'error': 'Database error'}), 500


# endpoint: POST /authors 
@authors_blueprint.route('/authors', methods=['POST'])
def create_author() -> dict:
    """
    Creates a new author.

    Returns:
        dict: JSON response with success message or error.
    """
    data = request.json
    if 'name' not in data or 'email' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        cursor = db.cursor()
        query = "INSERT INTO authors (name, email) VALUES (%s, %s)"
        cursor.execute(query, (data['name'], data['email']))
        db.commit()
        cursor.close()
        return jsonify({'message': 'Author created successfully'}), 201
    except Exception as e:
        logger.error(f"Error creating author: {str(e)}")
        return jsonify({'error': 'Database error'}), 500


# endpoint: PUT /authors/:id
@authors_blueprint.route('/authors/<int:author_id>', methods=['PUT'])
def update_author(author_id: int) -> dict:
    """
    Updates an existing author.

    Args:
        author_id (int): Author's ID.

    Returns:
        dict: JSON response with success message or error.
    """
    data = request.json
    if 'name' not in data or 'email' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        cursor = db.cursor()
        query = "SELECT * FROM authors WHERE id = %s"
        cursor.execute(query, (author_id,))
        author = cursor.fetchone()

        if not author:
            return jsonify({'error': 'Author not found'}), 404

        query = "UPDATE authors SET name = %s, email = %s WHERE id = %s"
        cursor.execute(query, (data['name'], data['email'], author_id))
        db.commit()
        cursor.close()

        query = "SELECT * FROM authors WHERE id = %s"
        cursor = db.cursor()
        cursor.execute(query, (author_id,))
        updated_author = cursor.fetchone()
        cursor.close()

        return jsonify({'message': 'Author updated successfully', 'author': {
            'id': updated_author[0],
            'name': updated_author[1],
            'email': updated_author[2]
        }}), 200
    except Exception as e:
        logger.error(f"Error updating author {author_id}: {str(e)}")
        return jsonify({'error': 'Database error'}), 500
 
    
# Delete Author (Soft Delete) 
# endpoint: DELETE /authors/:id
@authors_blueprint.route('/authors/<int:author_id>', methods=['DELETE'])
def delete_author(author_id: int) -> dict:
    """
    Soft deletes an author.

    Args:
        author_id (int): Author's ID.

    Returns:
        dict: JSON response with success message or error.
    """
    try:
        cursor = db.cursor()
        query = "SELECT * FROM authors WHERE id = %s AND is_deleted = 0"
        cursor.execute(query, (author_id,))
        author = cursor.fetchone()

        if not author:
            return jsonify({'error': 'Author not found or already deleted'}), 404

        query = "UPDATE authors SET is_deleted = 1 WHERE id = %s"
        cursor.execute(query, (author_id,))
        db.commit()
        cursor.close()

        return jsonify({'message': 'Author deleted successfully'}), 200
    except Exception as e:
        logger.error(f"Error deleting author {author_id}: {str(e)}")
        return jsonify({'error': 'Database error'}), 500


# endpoint: PATCH /authors/:id/restore
@authors_blueprint.route('/authors/<int:author_id>/restore', methods=['PATCH'])
def restore_author(author_id: int) -> dict:
    """
    Restores a soft-deleted author.

    Args:
        author_id (int): Author's ID.

    Returns:
        dict: JSON response with success message or error.
    """
    try:
        cursor = db.cursor()
        query = "SELECT * FROM authors WHERE id = %s"
        cursor.execute(query, (author_id,))
        author = cursor.fetchone()

        if not author:
            return jsonify({'error': 'Author not found'}), 404

        if author[3] == 0:  # Check if author is already active
            return jsonify({'error': 'Author is already active'}), 400

        query = "UPDATE authors SET is_deleted = 0 WHERE id = %s"
        cursor.execute(query, (author_id,))
        db.commit()
        cursor.close()

        return jsonify({'message': 'Author restored successfully'}), 200
    except Exception as e:
        logger.error(f"Error restoring author {author_id}: {str(e)}")
        return jsonify({'error': 'Database error'}), 500
        
        