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
# File Name         :       ./app/books.py
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

# books.py
'''
    API Endpoints Summary
        POST /books - Create book
        GET /books - Get all books
        GET /books/:id - Get book by ID
        PUT /books/:id - Update book
        DELETE /books/:id - Soft-delete book
        PATCH /books/:id/restore - Restore soft-deleted book
'''
 
from flask import Blueprint, jsonify, request
from .database import db  
import logging

books_blueprint = Blueprint('books', __name__)
logger = logging.getLogger(__name__)

# endpoint: GET /books
@books_blueprint.route('/books', methods=['GET'])
def get_books() -> dict:
    """
    Retrieve a list of books.

    Returns:
        dict: A dictionary containing a list of books.

    API Response:
        200 OK - List of books retrieved successfully.
        500 Internal Server Error - Database error occurred.

    Response Schema:
        {
            "books": [
                {
                    "id": int,
                    "title": str,
                    "author_id": int,
                    "publication_date": str
                }
            ]
        }
    """
    try:
        cursor = db.cursor()
        query = "SELECT * FROM books WHERE is_deleted = 0"
        cursor.execute(query)
        books = cursor.fetchall()
        cursor.close()
        return jsonify({'books': books})
    except Exception as e:
        logger.error(f"Error fetching books: {str(e)}")
        return jsonify({'error': 'Database error'}), 500


# New route: GET /books/:id
@books_blueprint.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id: int) -> dict:
    """
    Retrieves a book by ID.

    Args:
        book_id (int): Book's ID.

    Returns:
        dict: JSON response with book details or error.
    """
    try:
        cursor = db.cursor()
        query = "SELECT * FROM books WHERE id = %s AND is_deleted = 0"
        cursor.execute(query, (book_id,))
        book = cursor.fetchone()
        cursor.close()
        if book:
            return jsonify({'book': book})
        else:
            return jsonify({'error': 'Book not found'}), 404
    except Exception as e:
        logger.error(f"Error fetching book {book_id}: {str(e)}")
        return jsonify({'error': 'Database error'}), 500


# endpoint: POST /books 
@books_blueprint.route('/books', methods=['POST'])
def create_book() -> dict:
    """
    Creates a new book.

    Returns:
        dict: JSON response with success message or error.
    """
    data = request.json
    if 'title' not in data or 'author_id' not in data or 'publication_date' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        cursor = db.cursor()
        query = "INSERT INTO books (title, author_id, publication_date) VALUES (%s, %s, %s)"
        cursor.execute(query, (data['title'], data['author_id'], data['publication_date']))
        db.commit()
        cursor.close()
        return jsonify({'message': 'Book created successfully'}), 201
    except Exception as e:
        logger.error(f"Error creating book: {str(e)}")
        return jsonify({'error': 'Database error'}), 500


# endpoint: PUT /books/:id
@books_blueprint.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id: int) -> dict:
    """
    Updates an existing book.

    Args:
        book_id (int): Book's ID.

    Returns:
        dict: JSON response with success message or error.
    """
    data = request.json
    if 'title' not in data or 'author_id' not in data or 'publication_date' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        cursor = db.cursor()
        query = "SELECT * FROM books WHERE id = %s"
        cursor.execute(query, (book_id,))
        book = cursor.fetchone()

        if not book:
            return jsonify({'error': 'Book not found'}), 404

        query = "UPDATE books SET title = %s, author_id = %s, publication_date = %s WHERE id = %s"
        cursor.execute(query, (data['title'], data['author_id'], data['publication_date'], book_id))
        db.commit()
        cursor.close()

        query = "SELECT * FROM books WHERE id = %s"
        cursor = db.cursor()
        cursor.execute(query, (book_id,))
        updated_book = cursor.fetchone()
        cursor.close()

        return jsonify({'message': 'Book updated successfully', 'book': {
            'id': updated_book[0],
            'title': updated_book[1],
            'author_id': updated_book[2],
            'publication_date': updated_book[3]
        }}), 200
    except Exception as e:
        logger.error(f"Error updating book {book_id}: {str(e)}")
        return jsonify({'error': 'Database error'}), 500


# Delete Book (Soft Delete) 
# endpoint: DELETE /books/:id
@books_blueprint.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id: int) -> dict:
    """
    Soft deletes a book.

    Args:
        book_id (int): Book's ID.

    Returns:
        dict: JSON response with success message or error.
    """
    try:
        cursor = db.cursor()
        query = "SELECT * FROM books WHERE id = %s AND is_deleted = 0"
        cursor.execute(query, (book_id,))
        book = cursor.fetchone()

        if not book:
            return jsonify({'error': 'Book not found or already deleted'}), 404

        query = "UPDATE books SET is_deleted = 1 WHERE id = %s"
        cursor.execute(query, (book_id,))
        db.commit()
        cursor.close()

        return jsonify({'message': 'Book deleted successfully'}), 200
    except Exception as e:
        logger.error(f"Error deleting book {book_id}: {str(e)}")
        return jsonify({'error': 'Database error'}), 500


# endpoint: PATCH /books/:id/restore
@books_blueprint.route('/books/<int:book_id>/restore', methods=['PATCH'])
def restore_book(book_id: int) -> dict:
    """
    Restores a soft-deleted book.

    Args:
        book_id (int): Book's ID.

    Returns:
        dict: JSON response with success message or error.
    """
    try:
        cursor = db.cursor()
        query = "SELECT * FROM books WHERE id = %s"
        cursor.execute(query, (book_id,))
        book = cursor.fetchone()

        if not book:
            return jsonify({'error': 'Book not found'}), 404

        if book[4] == 0:  # Check if book is already active
            return jsonify({'error': 'Book is already active'}), 400

        query = "UPDATE books SET is_deleted = 0 WHERE id = %s"
        cursor.execute(query, (book_id,))
        db.commit()
        cursor.close()

        return jsonify({'message': 'Book restored successfully'}), 200
    except Exception as e:
        logger.error(f"Error restoring book {book_id}: {str(e)}")
        return jsonify({'error': 'Database error'}), 500