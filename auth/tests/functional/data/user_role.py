user_correct = {
    "username": "string",
    "password": "string123AAA",
    "email": "string@mail.com",
    "first_name": "string",
    "last_name": "string"
}


user_correct_del = {
    "username": "string_del",
    "password": "string123AAA",
    "email": "string_del@mail.com",
    "first_name": "string",
    "last_name": "string"
}

test_add_user_role_del = {
    "role_name": "test_role_del",
    "user_login": "string_del"
}

user_correct_1 = {
    "username": "string1",
    "password": "string123AAA",
    "email": "string1@mail.com",
    "first_name": "string",
    "last_name": "string"
}

test_add_user_role = {
    "role_name": "test_role",
    "user_login": "string"
}

test_add_user_role_answear = {
    "message": "UserRole was created for user_login <string> role_name <test_role>"
}


#
# test_add_user_role_answer_del = {
#     "message": "UserRole was created for user_login <string> role_name <test_role_del>"
# }


test_false_add_user_role = {
    "role_name": "test_role_1",
    "user_login": "string14353"
}

test_false_add_user_role_answear = {
    "message": "wrong data",
    "errors": [
        {
            "name": "Role name <test_role_1> or User login <string14353> doesn't exist"
        }
    ]
}

test1_delete_user_role_answear = {
    "message": 'UserRole was delete for user_login <string> role_name <test_role>'
}

test1_delete_user_role_answer_del = {
    "message": 'UserRole was delete for user_login <string_del> role_name <test_role_del>'
}

test2_delete_user_role_answear = {
    "message": "wrong data",
    "errors": [
        {
            "name": 'Role name <test_role_1> or User login <string14353> doesn\'t exist'
        }
    ]
}
