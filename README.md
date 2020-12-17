# Yggdrasil API
## What is Yggdrasil?
Yggdrasil is a content carousel display system, used for displaying carousels of pictures, videos, twitter feeds, and elements of the other systems within the Asgard System Stack.
Yggdrasil's back-end is a REST API microservice written in Python (v3), using the Flask microframework. The application was designed as a scalable microservice, providing reusable functionality within our internal System stack, Asgard.


Yggdrasil takes its name from Norse Mythology, where Yggdrasil is an "immense mythical tree that plays a central role in Norse cosmology, where it connects the Nine Worlds". The name was chosen as the system is designed to be able to pull data in from any of the other systems within the stack.

<br>

---

## Repository Structure
UNDER CONSTRUCTION

<br>

---

## Dependencies
The template uses the pip3 package manager and is written using Python3.

The following packages are used in the project:

### API - Flask - 1.0.3
Flask is the web microframework the application was developed to use as its core. It supplies all the main functionality and networking.

### API - Flask-RESTful - 0.3.7
Flask-RESTful is an extension to the Flask framework allowing for the easy configuration of REST architecture APIs. This handles our endpoint definition and opening the application up to the different query verb types.

### API - mysqlclient - 1.4.6
MySQL client is required for SQLAlchemy to interact with MySQL databases.

### API - Flask-SQLAlchemy - 2.4.0
Flask-SQLAlchemy is a Flask wrapper for the Object-Relational Mapper, SQLAlchemy. SQLAlchemy provides the toolset we use to interact with the MySQL database used by the API and provide a layer of security between the API and the raw data itself.

### API - Flask-Jsonpify - 1.5.0
Jsonify is our json parser, this package is what converts our result data from the database into the JSON responses we reply to our connected clients.

### API - Flask-Cors - 3.0.8
Flask-Cors is an extension package for routing and managing Cross-Origin Resource Sharing (CORS) across the application, and is mainly used to allow our web client to interact with the API itself.

### API - Webargs - 5.3.2
Webargs handles the parameter parsing from the endpoint URLs to usable data within our Flask resource objects, this library replaces the now depreciated "reqparse" from Flask-RESTful.

### API - Marshmellow - 3.0.1
Marshmellow is a dependency of Webargs, we had to freeze this at this version due to something on their end stopping working correctly.

### API - Nose2 - 0.9.1
Nose2 is an extension of the Python Unit-test module, we use this as part of our unit, feature and integration testing. The project is set to export the results of these tests as JUnit XML files.

<br>

---

## Commands
### Pip3
Batch Install the Pip3 modules at their frozen version by the following commands whilst in the projects root directory.
```pip3
pip3 install -r api/requirements.txt
```

<br>

---

## Testing
Under Construction

<br>

---

## Installation
Under Construction

<br>

---

## Usage Guide - API Interactions and Endpoints

### Exposed Endpoints
Valid Endpoints
```
<server_address>/yggdrasil-api/carousels
<server_address>/yggdrasil-api/carouselcontent
<server_address>/yggdrasil-api/carousel_handler
<server_address>/yggdrasil-api/content_handler
```

Example Endpoints
```
10.5.11.173/yggdrasil-api/carousels
10.5.11.173/yggdrasil-api/carouselcontent
10.5.11.173/yggdrasil-api/carousel_handler
10.5.11.173/yggdrasil-api/content_handler
```

### Endpoint - Carousels List
Usage:
```
<server_address>/yggdrasil-api/carousels

Supported HTTP Methods
* GET
```

params:
```
N/A
```

#### GET method
The GET method for the carousel list endpoint returns a JSON array listing the carousels registered with yggdrasil.

Usage:
```
GET -> <server_address>/yggdrasil-api/carousels
```

Example Response:
```JSON
{
    "meta":{},
    "links":{
        "self": "http://yggdrasil-api/carousels"
    },
    "data": {
        "carousels":[
            {
                "content": [],
                "id": 1,
                "name": "Example Carousel",
                "show_sidebar": true,
                "total_duration": 30000
            }
        ]
    }
}
```

### Endpoint - contents List
Usage:
```
<server_address>/yggdrasil-api/carouselcontent

Supported HTTP Methods
* GET
```

params:
```
carousel - (Optional) String name of the carousel to list the contents from.
```

#### GET method
The GET method for the contents list endpoint returns a JSON array listing the contents for a given carousel.

Usage:
```
GET -> <server_address>/yggdrasil-api/carouselcontent
GET -> <server_address>/yggdrasil-api/carouselcontent?carousel=carousel_example
```

Example Response:
```JSON
{
    "meta":{},
    "links":{
        "self": "http://yggdrasil-api/carouselcontent"
    },
    "data": {
        "carousel_content":[
            {
                "carousel": "Example Carousel",
                "carousel_id": 1,
                "id": 1,
                "interval": 15000,
                "is_enabled": true,
                "location": "Room A",
                "name": "Content Slide 1",
                "type": "mimir"
            }
        ]
    }
}
```

### Endpoint - Carousel Handler
Usage:
```
<server_address>/yggdrasil-api/carousel_handler

Supported HTTP Methods
* GET
* POST
* PUT
* DELETE
```

params:

GET
```
id - The integer id of the carousel to get
name - The friendly name for the carousel (id takes priority)
```

POST
```
name - The friendly name for the carousel
show_sidebar - Toggles the sidebar on the carousel (displays Uni logo, date and time)
```

PUT
```
id - The integer id of the carousel to update
show_sidebar - Toggles the sidebar on the carousel (displays Uni logo, date and time)
new_name - The new name for renaming the carousel
```

DELETE
```
id - The integer id of the carousel to delete
```

#### GET method
The GET method for the carousel_handler endpoint returns a JSON object representing a serialised version of the carousel.

Usage:
```
GET -> <server_address>/yggdrasil-api/carousel_handler?id=1
GET -> <server_address>/yggdrasil-api/carousel_handler?name=example_carousel
```

Response Codes:
```
200 - Ok
404 - carousel not found
422 - Invalid Parameters
```

Example Response:
```JSON
{
    "meta":{},
    "links":{
        "self": "http://yggdrasil-api:5000/carousel_handler?id=1"
    },
    "data":{
        "carousel":{
            "content":[],
            "id": 1,
            "name": "Example Carousel",
            "show_sidebar": true,
            "total_duration": 30000
        }
    }
}
```

#### POST method
The POST method for the carousel_handler endpoint allows the creation of a new carousel.

Usage:
```
POST -> <server_address>/yggdrasil-api/carousel_handler
```

Response Codes:
```
201 - Created
422 - Carousel of that name already exists
422 - Invalid Parameters
```

Example Request Body:
```JSON
{
    "name": "Example carousel",
    "show_sidebar": true
}
```

#### PUT method
The PUT method for the carousel_handler endpoint allows for changes to be made to a carousel's data.

Usage:
```
PUT -> <server_address>/yggdrasil-api/carousel_handler
```

Response Codes:
```
202 - Accepted
405 - Carousel does not exist
422 - Carousel of that name already exists
422 - Invalid Parameters
```

Example Request Body:
```JSON
{
    "id": 1,
    "name": "Renamed Example carousel",
    "show_sidebar": true
}
```

#### DELETE method
The DELETE method for the carousel_handler endpoint allows for the deletion of a specified carousel.

Usage:
```
DELETE -> <server_address>/yggdrasil-api/carousel_handler?id=1
```

Response Codes:
```
202 - Success
404 - Carousel not found
422 - Invalid Parameters
```
