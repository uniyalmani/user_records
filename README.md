# user_records

authentication and authorization

docker-compose up -> to run project locally

user can create account 
user can add name, college to db 
user can list all added name and college name

end point can be tested by postman as well as integrated UI.

end points 

"/" -> home
# "/login" --> type - post
'''
{ "data": {
    "email":"Ashu@1234",
    "password":"9410197255"
    }
}
'''

#"/signup" --> type - post

'''
{ "data": {
    "email":"Ashu@1234",
    "password":"9410197255",
    "username": "ashu"
    }
}
'''
# "/add_user"--> type - post

'''
{ "data": {
    "college":"Ashu@1234",
    "name":"9410197255"
    }
}
'''
