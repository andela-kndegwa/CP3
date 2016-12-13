[![Build Status](https://travis-ci.org/andela-kndegwa/CP3.svg?branch=ch-write-tests)](https://travis-ci.org/andela-kndegwa/CP3)
[![Coverage Status](https://coveralls.io/repos/github/andela-kndegwa/CP3/badge.svg?branch=ch-write-tests)](https://coveralls.io/github/andela-kndegwa/CP3?branch=ch-write-tests)
[![Kimani Ndegwa](https://img.shields.io/badge/Kimani%20Ndegwa-ThirdCheckpoint-9932CC.svg)]()

# ZUHURA BUCKET LIST API USING DJANGO.

>A project done in fulfillment of the third checkpoint of the Andela training program.

# PROJECT OVERVIEW

> Why Zuhura? Zuhura is swahili for the planet Venus. The general assumption here is after earth we just head on to Venus.


# SCOPE.

In this exercise, the task was to create a Django API for a bucket list service, complete with a front end , of which Angular was suggested as a preferred framework. I chose Angular 2 for this project and the front end implementation is well laid out in this repository. The  *Specification* for the API is as shown below.

METHOD | ENDPOINT | FUNCTIONALITY
--- | --- | ---
POST| /auth/login | Logs a user in
POST | /auth/register | Register a user
POST| /bucketlists| Create a new bucket list
GET|  /bucketlists | List all the created bucket lists
GET|  ```/bucketlists/<id>```| Get single bucket list
PUT| ```/bucketlists/<id>```| Update this bucket list
DELETE | ```/bucketlists/<id>```| Delete this single bucket list
POST| ```/bucketlists/<id>/items/```| Create a new item in bucket list
PUT |```/bucketlists/<id>/items/<item_id>```|Update item in bucket list
DELETE |```/bucketlists/<id>/items/<item_id>```| Delete item in bucket list

# INSTALLATION & SET UP.

1. First clone this repository to your local machine using  ```git clone https://github.com/andela-kndegwa/CP3.git```

2. Checkout into the **ch-write-tests** branch using ```git checkout ch-write-tests```

3. Create a ***virtual environment*** on your machine using  and install the dependencies via ```pip install -r requirements.txt``` after activating the virtual environment.

>The above steps allow you to get the project to your machine. Next, create the database using migrations and set it up as follows.

4. Change directories into the Zuhura folder I.e ```cd zuhura```

```python manage.py migrate```


>Now the project is fully set up with the database in place. Run the following command to get blister running:

```python manage.py runserver```

The server should be running on [http://127.0.0.1:8000] 

# USAGE.

For purposes of understanding how the API works, install the **Google Chrome** extension [Postman](https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop?hl=en).

>I have hosted the project at https://zuhura-api.herokuapp.com, for accessibility purposes and also to ensure the front end could consume this public API.

Once your up and running with postman, the following steps should get your acquainted with how the Zuhura API works:

- **Register a user.**

Copy the above link plus the **api/v1.0/auth/register/** appended to the tail end of the link. i.e:
**https://zuhura-api.herokuapp.com/api/v1.0/auth/register/**

- Ensure the dropdown to the left of the URL bar is a POST request

- In the body tab on Postman, enter a username, email and password in JSON format i.e:

```{"username":"demouser", "email":"demo@gmail.com", password":"pass"}```

***Set it by checking on the raw checkbox and clicking on application/json on the text drop down***

![Demo Image](/docs/1.png?raw=true)

A successful registration should return the message:

```
{
  "id": <id>,
  "username": "demouser",
  "email": "demo@gmail.com"
}
```

- **Login a user.**

This time the link changes to:
**https://zuhura-api.herokuapp.com/api/v1.0/auth/login**

- Ensure that the method is a POST request also and log in with the same credentials used to sign up.

```{"username":"demouser", "password":"pass"}```

![Demo Image](/docs/2.png?raw=true)

A successful login should return a token such as above, e.g :

```
{
  "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ3OTA1MDkyOCwiaWF0IjoxNDc5MDQ3MzI4fQ.eyJpZCI6NX0.I7XMV4jKhgczmSil9MwFpogyeDxlFvYc6ObFZTKsLZg"
}
```
Copy only the token as it will be used during the next step.

- **Create a bucketlist**

This project utilizes **Token Based Authentication** to restrict access to certain resources. Absence
of this token with the methods from here will result in a **401: Unauthorized Access** error.

To create a bucketlist, make a **POST** request to the following URI:
**https://zuhura-api.herokuapp.com/api/v1.0/bucketlists**.

In the headers tab ensure the following:

>Content-Type ----> application/json

>Authorization ---> **JWT** eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ3OTA1MDkyOCwiaWF0IjoxNDc5MDQ3MzI4fQ.eyJpZCI6NX0.I7XMV4jKhgczmSil9MwFpogyeDxlFvYc6ObFZTKsLZg

Ensure the ***JWT*** prefix comes before the token earlier copied.
Give your Bucketlist a name and hit send, e.g:

```
{
"name": "Demo bucket list title",
}
```

A successful request should be as follows:

![Demo Image](/docs/3.png?raw=true)

To view it you can make a **GET** request to the URI for bucketlists plus the ID of the bucketlists appended:

**https://zuhura-api.herokuapp.com/api/v1.0/bucketlists/ID**.


- **Update or Delete a bucketlist**

To **UPDATE** a bucketlist, navigate to the full link as stated above i.e:

**https://zuhura-api.herokuapp.com/api/v1.0/bucketlists/ID** with the method for the URL as **PUT.**

In the body tab, provide your information as follows:

```
{
"description":"This is a demo update for my earlier bucket list"
}
```
A successful update should be as follows:

![Demo Image](/docs/4.png?raw=true)

To **DELETE** a bucketlist, navigate to the full link as stated above i.e:

**https://zuhura-api.herokuapp.com/api/v1.0/bucketlists/ID** with the method for the URL as **DELETE**.

A successful request should return a HTTP 204 status code as follows:

![Demo Image](/docs/5.png?raw=true)

- **Creating a bucket list item**

To create a bucketlist item, make sure you have a bucketlist and navigate to the following url:

**https://zuhura-api.herokuapp.com/api/v1.0/bucketlists/ID/items** as a **POST** request.

> ID here represents the ID of the bucket list you want to add items to.

Add your content:

```
{
"name": "Demo bucket list item title",
}
```
A successful POST reqeuest should return the following:

![Demo Image](/docs/6.png?raw=true)

Make a **GET** request to view the item at the following URI:

**https://zuhura-api.herokuapp.com/api/v1.0/bucketlists/bucketlist_id/items/item_id**

- **Updating or deleting a bucket list item**

The format takes the same approach as the bucketlist update or delete with the only difference being the URI:

**https://zuhura-api.herokuapp.com/api/v1.0/bucketlists/bucketlist_id/items/item_id**


# TESTS.

The Zuhura API is tested and this can be confirmed by running the command

```
python manage.py test
```

### Contributors.

1. [Abdulmalik Abdulwahab.](https://github.com/andela-aabdulwahab)

2. [Chukwuerika Dike](https://github.com/andela-cdike)