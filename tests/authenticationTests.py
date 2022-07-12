from datetime  import datetime;
from jwt       import decode;
from requests  import request;
from data      import getUser;
from data      import setIsUserRegistered;
from utilities import equals;
from utilities import setUpPassFunction;
from utilities import setUpAdminHeaders;
from utilities import setUpUserHeaders;
from utilities import runTests;

def userRegisterEquals ( isBuyer ):
    def userRegisterEqualsImplementation ( setUpData, expectedResponse, receivedResponse ):
        equals ( setUpData, expectedResponse, receivedResponse );
        setIsUserRegistered ( isBuyer, True );

    return userRegisterEqualsImplementation;

def tokenTest ( response, user, tokenField, secret, expectedType, expectedSubject, expectedForename, expectedSurname, rolesField, expectedRole, expectedExpiresDelta ):
    assert tokenField in response, f"Login response error, {tokenField} field missing for user {user}.";

    token = decode ( response[tokenField], key = secret, algorithms = ["HS256"] );

    assert "nbf"      in token, f"{tokenField} error for user {user}, field nbf is missing."
    assert "type"     in token, f"{tokenField} error for user {user}, field type is missing."
    assert "exp"      in token, f"{tokenField} error for user {user}, field exp is missing."
    assert "sub"      in token, f"{tokenField} error for user {user}, field sub is missing."
    assert "forename" in token, f"{tokenField} error for user {user}, field forename is missing."
    assert "surname"  in token, f"{tokenField} error for user {user}, field surname is missing."
    assert rolesField in token, f"{tokenField} error for user {user}, field {rolesField} is missing."

    nbf      = token["nbf"]
    type     = token["type"]
    exp      = token["exp"]
    sub      = token["sub"]
    forename = token["forename"]
    surname  = token["surname"]
    roles    = token[rolesField]

    assert type     == expectedType                            , f"{tokenField} error for user {user}, field type has an incorrect value, expected {expectedType}, got {type}."
    assert sub      == expectedSubject                         , f"{tokenField} error for user {user}, field sub has an incorrect value, expected {expectedSubject}, got {sub}."
    assert forename == expectedForename                        , f"{tokenField} error for user {user}, field forename has an incorrect value, expected {expectedForename}, got {forename}."
    assert surname  == expectedSurname                         , f"{tokenField} error for user {user}, field surname has an incorrect value, expected {expectedSurname}, got {surname}."
    assert (roles   == expectedRole) or (expectedRole in roles), f"{tokenField} error for user {user}, field {rolesField} has an incorrect value, expected {expectedRole}, got {roles}."

    expiresDelta = datetime.fromtimestamp ( exp ) - datetime.fromtimestamp ( nbf );

    assert expiresDelta.total_seconds ( ) == expectedExpiresDelta, f"{tokenField} error for user {user}, expiration has an incorrect value, expected {expectedExpiresDelta}, got {expiresDelta.total_seconds ( )}."

def setUpRefreshRequest ( authenticationAddress, headers, email, password ):
    loginData = {
            "email"   : email,
            "password": password,
    };

    response = request (
            method  = "post",
            url     = authenticationAddress + "/login",
            headers = { },
            json    = loginData
    );

    headers["Authorization"] = "Bearer " + response.json ( )["refreshToken"];

def adminTokenTest ( response, tokenField, secret, expectedType, rolesField, expectedRole, expectedExpiresDelta ):
    tokenTest (
            response             = response,
            user                 = "admin",
            tokenField           = tokenField,
            secret               = secret,
            expectedType         = expectedType,
            expectedSubject      = "admin@admin.com",
            expectedForename     = "admin",
            expectedSurname      = "admin",
            rolesField           = rolesField,
            expectedRole         = expectedRole,
            expectedExpiresDelta = expectedExpiresDelta
    );

def adminAccessTokenTestWrapper ( response, secret, rolesField, expectedRole ):
    adminTokenTest (
            response             = response,
            tokenField           = "accessToken",
            secret               = secret,
            expectedType         = "access",
            rolesField           = rolesField,
            expectedRole         = expectedRole,
            expectedExpiresDelta = 60 * 60
    );

def adminRefreshTokenTestWrapper ( response, secret, rolesField, expectedRole ):
    adminTokenTest (
            response             = response,
            tokenField           = "refreshToken",
            secret               = secret,
            expectedType         = "refresh",
            rolesField           = rolesField,
            expectedRole         = expectedRole,
            expectedExpiresDelta = 30 * 24 * 60 * 60
    );

def adminAccessTokenTest ( jwtSecret, rolesField, administratorRole ):
    def adminAccessTokenTestImplementation ( setUpData, expectedResponse, receivedResponse ):
        adminAccessTokenTestWrapper (
                response     = receivedResponse,
                secret       = jwtSecret,
                rolesField   = rolesField,
                expectedRole = administratorRole
        );

    return adminAccessTokenTestImplementation;

def adminRefreshTokenTest ( jwtSecret, rolesField, administratorRole ):
    def adminRefreshTokenTestImplementation ( setUpData, expectedResponse, receivedResponse ):
        adminRefreshTokenTestWrapper (
                response     = receivedResponse,
                secret       = jwtSecret,
                rolesField   = rolesField,
                expectedRole = administratorRole
        );

    return adminRefreshTokenTestImplementation;

def setUpAdminRefreshRequest ( authenticationAddress ):
    def setUpAdminRefreshRequestImplementation ( url, headers, data, files ):
        setUpRefreshRequest (
                authenticationAddress = authenticationAddress,
                headers               = headers,
                email                 = "admin@admin.com",
                password              = "1"
        );

        return ( url, None, False );

    return setUpAdminRefreshRequestImplementation;

def userTokenTest ( isBuyer, response, tokenField, secret, expectedType, rolesField, expectedRole, expectedExpiresDelta ):
    tokenTest (
            response             = response,
            user                 = getUser ( isBuyer )["forename"] + getUser ( isBuyer )["surname"],
            tokenField           = tokenField,
            secret               = secret,
            expectedType         = expectedType,
            expectedSubject      = getUser ( isBuyer )["email"],
            expectedForename     = getUser ( isBuyer )["forename"],
            expectedSurname      = getUser ( isBuyer )["surname"],
            rolesField           = rolesField,
            expectedRole         = expectedRole,
            expectedExpiresDelta = expectedExpiresDelta
    );

def userAccessTokenTestWrapper ( isBuyer, response, secret, rolesField, expectedRole ):
    userTokenTest (
            isBuyer              = isBuyer,
            response             = response,
            tokenField           = "accessToken",
            secret               = secret,
            expectedType         = "access",
            rolesField           = rolesField,
            expectedRole         = expectedRole,
            expectedExpiresDelta = 60 * 60
    );

def userRefreshTokenTestWrapper ( isBuyer, response, secret, rolesField, expectedRole ):
    userTokenTest (
            isBuyer              = isBuyer,
            response             = response,
            tokenField           = "refreshToken",
            secret               = secret,
            expectedType         = "refresh",
            rolesField           = rolesField,
            expectedRole         = expectedRole,
            expectedExpiresDelta = 30 * 24 * 60 * 60
    );

def userAccessTokenTest ( isBuyer, jwtSecret, rolesField, userRole ):
    def userAccessTokenTestImplementation ( setUpData, expectedResponse, receivedResponse ):
        userAccessTokenTestWrapper (
                isBuyer      = isBuyer,
                response     = receivedResponse,
                secret       = jwtSecret,
                rolesField   = rolesField,
                expectedRole = userRole
        );

    return userAccessTokenTestImplementation;

def setUpUserRefreshRequest ( authenticationAddress, isBuyer ):
    def setUpUserRefreshRequestImplementation ( url, headers, data, files ):
        setUpRefreshRequest (
                authenticationAddress = authenticationAddress,
                headers               = headers,
                email                 = getUser ( isBuyer )["email"],
                password              = getUser ( isBuyer )["password"]
        );

        return ( url, None, False );

    return setUpUserRefreshRequestImplementation;

def userRefreshTokenTest ( isBuyer, jwtSecret, rolesField, userRole ):
    def userRefreshTokenTestImplementation ( setUpData, expectedResponse, receivedResponse ):
        userRefreshTokenTestWrapper (
                isBuyer      = isBuyer,
                response     = receivedResponse,
                secret       = jwtSecret,
                rolesField   = rolesField,
                expectedRole = userRole
        );

    return userRefreshTokenTestImplementation;


def userDeleteEquals ( isBuyer ):
    def userDeleteEqualsImplementation ( setUpData, expectedResponse, receivedResponse ):
        equals ( setUpData, expectedResponse, receivedResponse );
        setIsUserRegistered ( isBuyer, False );

    return userDeleteEqualsImplementation;


def runAuthenticationTests ( authenticationAddress, jwtSecret, rolesField, customerRole, managerRole, administratorRole ):
    tests = [
        # register errors
        ["post", authenticationAddress + "/register", setUpPassFunction, { }, {                                                                                                               }, { }, 400, { "message": "Field forename is missing."   }, equals, 1],
        ["post", authenticationAddress + "/register", setUpPassFunction, { }, { "forename": ""                                                                                                }, { }, 400, { "message": "Field forename is missing."   }, equals, 1],
        ["post", authenticationAddress + "/register", setUpPassFunction, { }, { "forename": " "                                                                                               }, { }, 400, { "message": "Field surname is missing."    }, equals, 1],
        ["post", authenticationAddress + "/register", setUpPassFunction, { }, { "forename": " "   , "surname": ""                                                                             }, { }, 400, { "message": "Field surname is missing."    }, equals, 1],
        ["post", authenticationAddress + "/register", setUpPassFunction, { }, { "forename": " "   , "surname": " "                                                                            }, { }, 400, { "message": "Field email is missing."      }, equals, 1],
        ["post", authenticationAddress + "/register", setUpPassFunction, { }, { "forename": " "   , "surname": " "  , "email": ""                                                             }, { }, 400, { "message": "Field email is missing."      }, equals, 1],
        ["post", authenticationAddress + "/register", setUpPassFunction, { }, { "forename": " "   , "surname": " "  , "email": " "                                                            }, { }, 400, { "message": "Field password is missing."   }, equals, 1],
        ["post", authenticationAddress + "/register", setUpPassFunction, { }, { "forename": " "   , "surname": " "  , "email": " "              , "password": ""                              }, { }, 400, { "message": "Field password is missing."   }, equals, 1],
        ["post", authenticationAddress + "/register", setUpPassFunction, { }, { "forename": "John", "surname": "Doe", "email": " "              , "password": " "                             }, { }, 400, { "message": "Field isCustomer is missing." }, equals, 1],
        ["post", authenticationAddress + "/register", setUpPassFunction, { }, { "forename": "John", "surname": "Doe", "email": " "              , "password": " "        , "isCustomer": True }, { }, 400, { "message": "Invalid email."               }, equals, 1],
        ["post", authenticationAddress + "/register", setUpPassFunction, { }, { "forename": "John", "surname": "Doe", "email": "john"           , "password": " "        , "isCustomer": True }, { }, 400, { "message": "Invalid email."               }, equals, 1],
        ["post", authenticationAddress + "/register", setUpPassFunction, { }, { "forename": "John", "surname": "Doe", "email": "john@"          , "password": " "        , "isCustomer": True }, { }, 400, { "message": "Invalid email."               }, equals, 1],
        ["post", authenticationAddress + "/register", setUpPassFunction, { }, { "forename": "John", "surname": "Doe", "email": "john@gmail"     , "password": " "        , "isCustomer": True }, { }, 400, { "message": "Invalid email."               }, equals, 1],
        ["post", authenticationAddress + "/register", setUpPassFunction, { }, { "forename": "John", "surname": "Doe", "email": "john@gmail."    , "password": " "        , "isCustomer": True }, { }, 400, { "message": "Invalid email."               }, equals, 1],
        ["post", authenticationAddress + "/register", setUpPassFunction, { }, { "forename": "John", "surname": "Doe", "email": "john@gmail.a"   , "password": " "        , "isCustomer": True }, { }, 400, { "message": "Invalid email."               }, equals, 1],
        ["post", authenticationAddress + "/register", setUpPassFunction, { }, { "forename": "John", "surname": "Doe", "email": "john@gmail.com" , "password": " "        , "isCustomer": True }, { }, 400, { "message": "Invalid password."            }, equals, 1],
        ["post", authenticationAddress + "/register", setUpPassFunction, { }, { "forename": "John", "surname": "Doe", "email": "john@gmail.com" , "password": "aaaaaaaa" , "isCustomer": True }, { }, 400, { "message": "Invalid password."            }, equals, 1],
        ["post", authenticationAddress + "/register", setUpPassFunction, { }, { "forename": "John", "surname": "Doe", "email": "john@gmail.com" , "password": "aaaaaaaaa", "isCustomer": True }, { }, 400, { "message": "Invalid password."            }, equals, 1],
        ["post", authenticationAddress + "/register", setUpPassFunction, { }, { "forename": "John", "surname": "Doe", "email": "john@gmail.com" , "password": "Aaaaaaaaa", "isCustomer": True }, { }, 400, { "message": "Invalid password."            }, equals, 1],
        ["post", authenticationAddress + "/register", setUpPassFunction, { }, { "forename": "John", "surname": "Doe", "email": "admin@admin.com", "password": "Aaaaaaaa1", "isCustomer": True }, { }, 400, { "message": "Email already exists."        }, equals, 1],

        # login errors
        ["post", authenticationAddress + "/login", setUpPassFunction, { }, {                                              }, { }, 400, { "message": "Field email is missing."    }, equals, 1],
        ["post", authenticationAddress + "/login", setUpPassFunction, { }, { "email": ""                                  }, { }, 400, { "message": "Field email is missing."    }, equals, 1],
        ["post", authenticationAddress + "/login", setUpPassFunction, { }, { "email": " "                                 }, { }, 400, { "message": "Field password is missing." }, equals, 1],
        ["post", authenticationAddress + "/login", setUpPassFunction, { }, { "email": " "             , "password": ""    }, { }, 400, { "message": "Field password is missing." }, equals, 1],
        ["post", authenticationAddress + "/login", setUpPassFunction, { }, { "email": "john"          , "password": " "   }, { }, 400, { "message": "Invalid email."             }, equals, 1],
        ["post", authenticationAddress + "/login", setUpPassFunction, { }, { "email": "john@"         , "password": " "   }, { }, 400, { "message": "Invalid email."             }, equals, 1],
        ["post", authenticationAddress + "/login", setUpPassFunction, { }, { "email": "john@gmail"    , "password": " "   }, { }, 400, { "message": "Invalid email."             }, equals, 1],
        ["post", authenticationAddress + "/login", setUpPassFunction, { }, { "email": "john@gmail."   , "password": " "   }, { }, 400, { "message": "Invalid email."             }, equals, 1],
        ["post", authenticationAddress + "/login", setUpPassFunction, { }, { "email": "john@gmail.a"  , "password": " "   }, { }, 400, { "message": "Invalid email."             }, equals, 1],
        ["post", authenticationAddress + "/login", setUpPassFunction, { }, { "email": "john@gmail.com", "password": "123" }, { }, 400, { "message": "Invalid credentials."       }, equals, 1],

        # refresh errors
        ["post", authenticationAddress + "/refresh", setUpPassFunction, { }, { }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],

        # delete errors
        ["post", authenticationAddress + "/delete", setUpPassFunction                                      , { }, {                           }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],
        ["post", authenticationAddress + "/delete", setUpAdminHeaders ( True, authenticationAddress )      , { }, {                           }, { }, 400, { "message": "Field email is missing."  }, equals, 1],
        ["post", authenticationAddress + "/delete", setUpAdminHeaders ( True, authenticationAddress )      , { }, { "email": ""               }, { }, 400, { "message": "Field email is missing."  }, equals, 1],
        ["post", authenticationAddress + "/delete", setUpAdminHeaders ( True, authenticationAddress )      , { }, { "email": "john@"          }, { }, 400, { "message": "Invalid email."           }, equals, 1],
        ["post", authenticationAddress + "/delete", setUpAdminHeaders ( True, authenticationAddress )      , { }, { "email": "john@gmail"     }, { }, 400, { "message": "Invalid email."           }, equals, 1],
        ["post", authenticationAddress + "/delete", setUpAdminHeaders ( True, authenticationAddress )      , { }, { "email": "john@gmail."    }, { }, 400, { "message": "Invalid email."           }, equals, 1],
        ["post", authenticationAddress + "/delete", setUpAdminHeaders ( True, authenticationAddress )      , { }, { "email": "john@gmail.a"   }, { }, 400, { "message": "Invalid email."           }, equals, 1],
        ["post", authenticationAddress + "/delete", setUpAdminHeaders ( True, authenticationAddress )      , { }, { "email": "john@gmail.a"   }, { }, 400, { "message": "Invalid email."           }, equals, 1],
        ["post", authenticationAddress + "/delete", setUpAdminHeaders ( True, authenticationAddress )      , { }, { "email": "john@gmail.com" }, { }, 400, { "message": "Unknown user."            }, equals, 1],
        ["post", authenticationAddress + "/delete", setUpUserHeaders ( True, True, authenticationAddress ) , { }, {                           }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],
        ["post", authenticationAddress + "/delete", setUpUserHeaders ( True, False, authenticationAddress ), { }, {                           }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],

        # user delete
        ["post", authenticationAddress + "/delete", setUpAdminHeaders ( True, authenticationAddress ), { }, { "email": getUser ( True )["email"]  }, { }, 200, None, userDeleteEquals ( True ) , 2],
        ["post", authenticationAddress + "/delete", setUpAdminHeaders ( True, authenticationAddress ), { }, { "email": getUser ( False )["email"] }, { }, 200, None, userDeleteEquals ( False ), 2],

        ["post", authenticationAddress + "/login", setUpPassFunction , { }, { "email": getUser ( True )["email"], "password": getUser ( True )["password"]   }, { }, 400, { "message": "Invalid credentials." }, equals, 5],
        ["post", authenticationAddress + "/login", setUpPassFunction , { }, { "email": getUser ( False )["email"], "password": getUser ( False )["password"] }, { }, 400, { "message": "Invalid credentials." }, equals, 5],

        # admin login
        ["post", authenticationAddress + "/login", setUpPassFunction, { }, { "email": "admin@admin.com", "password": "1" }, { }, 200, { }, adminAccessTokenTest ( jwtSecret, rolesField, administratorRole ) , 3],
        ["post", authenticationAddress + "/login", setUpPassFunction, { }, { "email": "admin@admin.com", "password": "1" }, { }, 200, { }, adminRefreshTokenTest ( jwtSecret, rolesField, administratorRole ), 3],

        # user register
        ["post", authenticationAddress + "/register", setUpPassFunction, { }, getUser ( True ) , { }, 200, None, userRegisterEquals ( True ) , 7],
        ["post", authenticationAddress + "/register", setUpPassFunction, { }, getUser ( False ), { }, 200, None, userRegisterEquals ( False ), 7],

        # user login
        ["post", authenticationAddress + "/login", setUpPassFunction, { }, { "email": getUser ( True ) ["email"], "password": getUser ( True ) ["password"] }, { }, 200, { }, userAccessTokenTest ( True, jwtSecret, rolesField, customerRole ) , 3],
        ["post", authenticationAddress + "/login", setUpPassFunction, { }, { "email": getUser ( True ) ["email"], "password": getUser ( True ) ["password"] }, { }, 200, { }, userRefreshTokenTest ( True, jwtSecret, rolesField, customerRole ), 3],

        ["post", authenticationAddress + "/login", setUpPassFunction, { }, { "email": getUser ( False )["email"], "password": getUser ( False )["password"] }, { }, 200, { }, userAccessTokenTest ( False, jwtSecret, rolesField, managerRole ) , 3],
        ["post", authenticationAddress + "/login", setUpPassFunction, { }, { "email": getUser ( False )["email"], "password": getUser ( False )["password"] }, { }, 200, { }, userRefreshTokenTest ( False, jwtSecret, rolesField, managerRole ), 3],

        # admin refresh
        ["post", authenticationAddress + "/refresh", setUpAdminRefreshRequest ( authenticationAddress ), { }, { }, { }, 200, { }, adminAccessTokenTest ( jwtSecret, rolesField, administratorRole ), 2],

        # user refresh
        ["post", authenticationAddress + "/refresh", setUpUserRefreshRequest ( authenticationAddress, True ) , { }, { }, { }, 200, { }, userAccessTokenTest ( True, jwtSecret, rolesField, customerRole ), 2],
        ["post", authenticationAddress + "/refresh", setUpUserRefreshRequest ( authenticationAddress, False ), { }, { }, { }, 200, { }, userAccessTokenTest ( False, jwtSecret, rolesField, managerRole ), 2],
    ];

    percentage = runTests ( tests );

    return percentage;
