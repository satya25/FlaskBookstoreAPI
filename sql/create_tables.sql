-- File name: create_tables.sql
-- Purpose: Creates tables for the bookstore database.


-- Switch to the 'bookstore_db' database.
USE bookstore_db;


-- Create the 'authors' table.
CREATE TABLE authors (
  -- Unique identifier for the author.
  id INT AUTO_INCREMENT,
  -- Author's name.
  name VARCHAR(255) NOT NULL,
  -- Author's email (unique).
  email VARCHAR(255) UNIQUE,
  -- Primary key for the table.
  PRIMARY KEY (id)
);
 
-- Create the 'books' table.
CREATE TABLE books (
  -- Unique identifier for the book.
  id INT AUTO_INCREMENT,
  -- Book title.
  title VARCHAR(255) NOT NULL,
  -- Foreign key referencing the 'authors' table.
  author_id INT,
  -- Book publication date.
  publication_date DATE,
  -- Primary key for the table.
  PRIMARY KEY (id),
  -- Establish the relationship between 'books' and 'authors'.
  FOREIGN KEY (author_id) REFERENCES authors(id)
);


-- Add a 'is_deleted' flag to the 'authors' table for soft deletion.
ALTER TABLE authors
ADD COLUMN is_deleted TINYINT(1) DEFAULT 0;

-- Add a 'is_deleted' flag to the 'books' table for soft deletion.
ALTER TABLE books
ADD COLUMN is_deleted TINYINT(1) DEFAULT 0;
