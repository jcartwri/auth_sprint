test_role_create = {
    "role_name": "test_role"
}

test_role_create_del = {
    "role_name": "test_role_del"
}

test_role_create_mess = {
    "message": "Role name <test_role> was created"
}


test_role_create_2 = {
    "role_name": "test_role_2"
}

test_role_create_mess_2 = {
    "message": "Role name <test_role_2> was created"
}

test_role_create_3 = {
    "role_name": "test_role_3"
}

test_role_create_mess_3 = {
    "message": "Role name <test_role_3> was created"
}


test_role_create_1 = {
    "role_name": "test_role_1"
}



false_test_role_create = {
    "role_name": ""
}

false_test_role_create_mess = {
    "message": "wrong data",
    "errors": [
        {
            "name": "This field must be not empty"
        }
    ]
}

test_role_delete = {
    "role_name": "test_role"
}

test_role_delete_mess = {
    "message": "Role name <test_role> was delete"
}

create_role_for_change_test1 = {
    "role_name": "test_role"
}

test_role_change = {
    "old_role_name": "test_role",
    "new_role_name": "new_test_role"
}

test_role_change_mess = {
    "message": "Role name <test_role> was change on <new_test_role>"
}

create_role_for_change_test2 = {
    "role_name": "false_role"
}

false_test_role_change = {
    "old_role_name": "false_role",
    "new_role_name": "new_test_role"
}

false_test_role_change_mess = {
    "message": "wrong data",
    "errors": [
        {
            "name": "Role name <false_role> doesn't exist"
        }
    ]
}