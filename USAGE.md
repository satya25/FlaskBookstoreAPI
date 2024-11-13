# API Usage
==========


## Table of Contents
-----------------

1. [Authors Endpoints](#authors-endpoints)
2. [Example Requests](#example-requests)


## Authors Endpoints
------------------


The following endpoints are available for authors:


### Get All Authors

* Method: GET
* Endpoint: /authors
* Description: Retrieve all authors

### Get Author by ID

* Method: GET
* Endpoint: /authors/:id
* Description: Retrieve author by ID

### Create New Author

* Method: POST
* Endpoint: /authors
* Description: Create new author
* Request Body:
	+ name (string)
	+ email (string)

### Update Author

* Method: PUT
* Endpoint: /authors/:id
* Description: Update author
* Request Body:
	+ name (string)
	+ email (string)

### Delete Author

* Method: DELETE
* Endpoint: /authors/:id
* Description: Delete author

### Restore Deleted Author

* Method: PATCH
* Endpoint: /authors/:id/restore
* Description: Restore deleted author


## Example Requests
------------------


### Using curl 

 
# Get all authors
curl http://localhost:5000/authors

# Create new author
curl -X POST -H "Content-Type: application/json" -d '{"name": "New Author", "email": "new@author.com"}' http://localhost:5000/authors

# Update author
curl -X PUT -H "Content-Type: application/json" -d '{"name": "Updated Author", "email": "updated@author.com"}' http://localhost:5000/authors/1

# Delete author
curl -X DELETE http://localhost:5000/authors/1

# Restore deleted author
curl -X PATCH http://localhost:5000/authors/1/restore

### Using Browser 

#### Accessing Endpoints
Simply navigate to the corresponding endpoint URLs in your web browser.

#### Additional Information
For detailed API documentation, please refer to [DOCUMENTATION.md](DOCUMENTATION.md).


#### Important Note
Replace `http://localhost:5000` with your actual application URL.