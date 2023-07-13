# user_records

* authentication and authorization

* docker-compose up -> to run project locally

* user can create account 
* user can add document with -  title, file, description 
* user can list all added documents
* user can filter beased on specific user and title

* end point can be tested by postman as well as integrated UI.

* end points 

# "/" -> home
# "/login" --> type - post
*** request body***
```
{ "data": {
    "email":"Ashu@1234",
    "password":"9410197255"
    }
}
```

# "/signup" --> type - post
*** request body***
```
{ "data": {
    "email":"Ashu@1234",
    "password":"9410197255",
    "username": "ashu"
    }
}
```

