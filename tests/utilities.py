import time;
import re;
import datetime;
from dateutil import parser;

from requests import request;
from copy     import deepcopy;
from data     import getUser;
from data     import getIsUserRegistered;
from data     import setIsUserRegistered;

def recursiveCompare ( expected, received, level = 'root', preprocessList = None, preprocessScalar = None ):
    message = "";
    same = True;

    if ( isinstance ( expected, dict ) and isinstance ( received, dict ) ):
        if ( sorted ( expected.keys ( ) ) != sorted ( received.keys ( ) ) ):
            expectedKeySet = set ( expected.keys ( ) );
            receivedKeySet = set ( received.keys ( ) );

            message += "{:<20} +{} -{}\n".format ( level, expectedKeySet - receivedKeySet, receivedKeySet - expectedKeySet );
            same = False;

            commonKeys = expectedKeySet & receivedKeySet;
        else:
            commonKeys = set ( expected.keys ( ) );

        for key in commonKeys:
            result = recursiveCompare (
                expected[key],
                received[key],
                "{}.{}".format ( level, key ),
                preprocessList,
                preprocessScalar
            );

            message += result[0];
            same    &= result[1];

    elif (isinstance ( expected, list ) and isinstance ( received, list )):
        if (len ( expected ) != len ( received )):
            message += "{:<20} expectedLength={}; receivedLength={}\n".format ( level, len ( expected ), len ( received ) );
            same = False;
        else:
            if ( preprocessList ):
                ( expected, received ) = preprocessList ( expected, received, level );

            for i in range ( len ( expected ) ):
                result = recursiveCompare (
                    expected[i],
                    received[i],
                    '{}[{}]'.format ( level, i ),
                    preprocessList,
                    preprocessScalar
                );

                message += result[0];
                same &= result[1];
    else:
        if ( preprocessScalar ):
            ( expected, received ) = preprocessScalar ( expected, received, level );

        if (expected != received):
            message += "{:<20} {} != {}\n".format ( level, expected, received );
            same = False;

    return ( message, same );

def copyDictionary ( destination, source ):
    for key in source:
        destination [key] = deepcopy ( source [key] );

def areEqual ( list0, list1 ):
    difference = [item for item in (list0 + list1) if ((item not in list0) or (item not in list1))];

    return len ( difference ) == 0;


def setUpPassFunction ( url, headers, data, files ):
    return (url, None, False);


def setUpAuthorizationErrorRequest ( withAuthentication ):
    def setUpAuthorizationErrorRequestImplementation ( url, headers, data, files ):
        if (not withAuthentication):
            return (url, None, True);

        return (url, None, False);

    return setUpAuthorizationErrorRequestImplementation;


def adminLogin ( authenticationAddress, headers ):
    response = request (
            method  = "post",
            url     = authenticationAddress + "/login",
            headers = { },
            json    = {
                    "email"   : "admin@admin.com",
                    "password": "1"
            }
    );

    headers ["Authorization"] = "Bearer " + response.json ( ) ["accessToken"];


def setUpAdminHeaders ( withAuthentication, authenticationAddress ):
    def setUpAdminHeadersImplementation ( url, headers, data, files ):
        if (withAuthentication):
            adminLogin ( authenticationAddress, headers );
        return (url, None, False);

    return setUpAdminHeadersImplementation;


def userLogin ( isCustomer, authenticationAddress, headers ):
    if (not getIsUserRegistered ( isCustomer )):
        response = request (
                method  = "post",
                url     = authenticationAddress + "/register",
                headers = { },
                json    = getUser ( isCustomer )
        );
        setIsUserRegistered ( isCustomer, True );

    response = request (
            method  = "post",
            url     = authenticationAddress + "/login",
            headers = { },
            json    = {
                    "email"   : getUser ( isCustomer ) ["email"],
                    "password": getUser ( isCustomer ) ["password"]
            }
    );

    headers ["Authorization"] = "Bearer " + response.json ( ) ["accessToken"];


def setUpUserHeaders ( withAuthentication, isCustomer, authenticationAddress ):
    def setUpUserHeadersImplementation ( url, headers, data, files ):
        if (withAuthentication):
            userLogin ( isCustomer, authenticationAddress, headers );

        return (url, "", False);

    return setUpUserHeadersImplementation;


def equals ( setUpData, expectedResponse, receivedResponse ):
    assert expectedResponse == receivedResponse, f"Invalid response, expected {expectedResponse}, received {receivedResponse}.";


def findFirst ( list, predicate ):
    for item in list:
        if ( predicate ( item ) ):
            return item;
    return None;

PATH = "temp.csv";

def createFile ( path, content ):
    with open ( path, "w" ) as file:
        file.write ( content );

def setUpUpdateTest ( withAuthentication, authenticationAddress, lines ):
    def setUpdateTestImplementation ( url, headers, data, files ):
        if ( withAuthentication ):
            userLogin ( False, authenticationAddress, headers );

        createFile ( PATH, lines );
        file          = open ( PATH, "r" );
        files["file"] = file;

        return ( url, None, False );

    return setUpdateTestImplementation;

def updateTestEquals ( setUpData, expectedResponse, receivedResponse ):
    equals ( setUpData, expectedResponse, receivedResponse );
    time.sleep ( 1 );

def setUpSearchTest ( withAuthentication, authenticationAddress, parameters ):
    def setUpdateErrorTestImplementation ( url, headers, data, files ):
        if ( withAuthentication ):
            userLogin ( True, authenticationAddress, headers );

        return ( url + "?" + parameters, "", False  );

    return setUpdateErrorTestImplementation;

def evaluateSearchTest ( setUpData, expectedResponse, receivedResponse ):
    def preprocessList ( expected, received, level ):
        result = re.match (
            pattern = r"root.products\[\d\].categories",
            string = level,
        );

        isProducts   = level == "root.products";
        isCategories = ( result != None ) or ( level == "root.categories" );

        if (isProducts):
            sortedExpected = sorted (
                expected,
                key = lambda item: item["name"]
            );
            sortedReceived = sorted (
                received,
                key = lambda item: item["name"]
            );

            return (list ( sortedExpected ), list ( sortedReceived ));
        elif (isCategories):
            sortedExpected = sorted ( expected );
            sortedReceived = sorted ( received );

            return (list ( sortedExpected ), list ( sortedReceived ));
        else:
            return (expected, received);

    def preprocessScalar ( expected, received, level ):
        result = re.match (
            pattern = r"root.products\[\d\].id",
            string = level,
        );

        isID = result != None;

        if (isID):
            if (type ( received ) is int):
                return (1, 1);
            else:
                return (expected, received);
        else:
            return (expected, received);


    ( message, same ) = recursiveCompare ( expectedResponse, receivedResponse, preprocessList = preprocessList, preprocessScalar = preprocessScalar );

    assert same, message;

def getEmptySearchResults ( withAuthentication, authenticationAddress, buyerAddress ):
    headers = { };
    if (withAuthentication):
        userLogin ( True, authenticationAddress, headers );

    response = request (
        method  = "get",
        url     = buyerAddress + "/search",
        headers = headers,
        json    = { }
    );

    return response.json ( );

def setUpOrderTest ( withAuthentication, authenticationAddress, buyerAddress ):
    def setUpdateErrorTestImplementation ( url, headers, data, files ):
        if ( withAuthentication ):
            userLogin ( True, authenticationAddress, headers );

        searchResult = getEmptySearchResults ( withAuthentication, authenticationAddress, buyerAddress );

        products = searchResult["products"];

        for index, request in enumerate ( data["requests"] ):
            product = findFirst ( products, lambda item: item["name"] == request["id"] );

            data["requests"][index]["id"] = product["id"];

        return ( url, "", False  );

    return setUpdateErrorTestImplementation;

def evaluateStatusTest ( setUpData, expectedResponse, receivedResponse ):
    def preprocessList ( expected, received, level ):
        productsResult = re.match (
            pattern = r"^root.orders\[\d\].products$",
            string  = level,
        );

        categoriesResult = re.match (
            pattern = r"root.orders\[\d\].products\[\d\].categories",
            string  = level,
        );

        isProducts   = productsResult != None;
        isCategories = categoriesResult != None;

        if ( isProducts ):
            sortedExpected = sorted (
                expected,
                key = lambda item: item["name"]
            );
            sortedReceived = sorted (
                received,
                key = lambda item: item["name"]
            );

            return (list ( sortedExpected ), list ( sortedReceived ));
        elif ( isCategories ):
            sortedExpected = sorted ( expected );
            sortedReceived = sorted ( received );

            return (list ( sortedExpected ), list ( sortedReceived ));
        else:
            return (expected, received);

    def preprocessScalar ( expected, received, level ):
        result = re.match (
            pattern = r"root.orders\[\d\].timestamp",
            string = level,
        );

        isTimestamp = result != None;

        if ( isTimestamp ):
            try:
                now          = datetime.datetime.now ( );
                receivedTime = parser.parse ( received );

                sameYear  = now.year == receivedTime.year;
                sameMonth = now.month == receivedTime.month;
                sameDay   = now.day == receivedTime.day;

                if ( ( not sameYear ) or ( not sameMonth ) or ( not sameDay ) ):
                    return (1, 2);
                else:
                    return ( 1, 1 );
            except ValueError as error:
                return ( 1, 2 );
        else:
            return ( expected, received );


    ( message, same ) = recursiveCompare ( expectedResponse, receivedResponse, preprocessList = preprocessList, preprocessScalar = preprocessScalar );

    assert same, message;

def evaluateProductStatisticsTest ( setUpData, expectedResponse, receivedResponse ):
    def preprocessList ( expected, received, level ):
        isStatistics = level == "root.statistics";

        if ( isStatistics ):
            sortedExpected = sorted (
                expected,
                key = lambda item: item["name"]
            );
            sortedReceived = sorted (
                received,
                key = lambda item: item["name"]
            );

            return ( list ( sortedExpected ), list ( sortedReceived ) );
        else:
            return ( expected, received );


    ( message, same ) = recursiveCompare ( expectedResponse, receivedResponse, preprocessList = preprocessList );

    assert same, message;

def evaluateCategoryStatisticsTest ( setUpData, expectedResponse, receivedResponse ):
    ( message, same ) = recursiveCompare ( expectedResponse, receivedResponse );

    assert same, message;

def evaluateOrderTest ( setUpData, expectedResponse, receivedResponse ):
    assert "id" in receivedResponse, "Missing field id.";
    assert type ( receivedResponse["id"] ) is int, "ID must an integer greater than or equal to 0."
    assert int ( receivedResponse["id"] ) >= 0, "ID must an integer greater than or equal to 0."

    time.sleep ( 1 );

def runTests ( tests ):
    max   = 0;
    total = 0;

    for index, test in enumerate ( tests ):
        method                 = test [0];
        url                    = test [1];
        preparationFunction    = test [2];
        headers                = test [3];
        data                   = test [4];
        files                  = test [5];
        expectedStatusCode     = test [6];
        expectedResponse       = test [7];
        testAndCleanupFunction = test [8];
        score                  = test [9];

        max   += score
        total += score;

        try:
            (url, setUpData, skipTest) = preparationFunction ( url, headers, data, files );

            if (not skipTest):
                response = request (
                        method  = method,
                        url     = url,
                        headers = headers,
                        json    = data,
                        files   = files
                );

                for key in files:
                    files [key].close ( );

                assert response.status_code == expectedStatusCode, f"Invalid status code, expected {expectedStatusCode}, received {response.status_code}";

                if (expectedResponse is not None):
                    receivedResponse = response.json ( );
                else:
                    expectedResponse = { };
                    receivedResponse = { };

                testAndCleanupFunction ( setUpData, expectedResponse, receivedResponse );

        except Exception as error:
            print ( f"Failed test number {index}\n\t method = {method}\n\t url = {url}\n\t headers = {headers}\n\t data = {data}\n\t files = {files}\n\t error: {error}" );
            total -= score;

    return total / max if (max != 0) else 0;
