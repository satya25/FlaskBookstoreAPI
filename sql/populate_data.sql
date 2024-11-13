-- File name: populate_data.sql
-- Purpose: Populates the database with sample data.


-- Switch to the 'bookstore_db' database.
USE bookstore_db;


-- Insert sample authors into the 'authors' table.
INSERT INTO authors (name, email) 
VALUES 
  -- Author 1: J.K. Rowling
  ('J.K. Rowling', 'jkrowling@example.com'),
  -- Author 2: J.R.R. Tolkien
  ('J.R.R. Tolkien', 'jrrtolkien@example.com'),
  -- Author 3: George R.R. Martin
  ('George R.R. Martin', 'georgermartin@example.com');


-- Insert sample books into the 'books' table.
INSERT INTO books (title, author_id, publication_date) 
VALUES 
  -- Book 1: Harry Potter and the Philosopher's Stone by J.K. Rowling
  ('Harry Potter and the Philosopher\'s Stone', 1, '1997-06-26'),
  -- Book 2: The Lord of the Rings by J.R.R. Tolkien
  ('The Lord of the Rings', 2, '1954-07-29'),
  -- Book 3: A Game of Thrones by George R.R. Martin
  ('A Game of Thrones', 3, '1996-08-01'),
  -- Book 4: Harry Potter and the Chamber of Secrets by J.K. Rowling
  ('Harry Potter and the Chamber of Secrets', 1, '1998-07-02'),
  -- Book 5: The Two Towers by J.R.R. Tolkien
  ('The Two Towers', 2, '1955-01-11');