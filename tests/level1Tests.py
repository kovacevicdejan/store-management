from utilities import equals;
from utilities import runTests;
from utilities import setUpAuthorizationErrorRequest;
from utilities import setUpAdminHeaders;
from utilities import setUpUserHeaders;
from utilities import evaluateSearchTest;
from utilities import setUpUpdateTest;
from utilities import updateTestEquals;
from utilities import setUpOrderTest;
from utilities import evaluateStatusTest;
from utilities import evaluateOrderTest;
from data      import getOrderError0;
from data      import getOrderError1;
from data      import getOrderError2;
from data      import getOrderError3;
from data      import getOrderError4;
from data      import getOrderError5;
from data      import getOrderError6;
from data      import getOrder0;
from data      import getOrderStatus0;
from data      import getSearchResult5;
from data      import getData2;
from data      import getOrder1;
from data      import getOrderStatus1;
from data      import getSearchResult6;

def runLevel1Tests ( withAuthentication, authenticationAddress, warehouseAddress, customerAddress ):

    tests = [
        # order errors
        ["post", customerAddress + "/order", setUpAuthorizationErrorRequest ( withAuthentication )                , { }, { }               , { }, 401, { "msg": "Missing Authorization Header"                          }, equals, 1],
        ["post", customerAddress + "/order", setUpAdminHeaders ( withAuthentication, authenticationAddress )      , { }, { }               , { }, 401, { "msg": "Missing Authorization Header"                          }, equals, 1],
        ["post", customerAddress + "/order", setUpUserHeaders ( withAuthentication, False, authenticationAddress ), { }, { }               , { }, 401, { "msg": "Missing Authorization Header"                          }, equals, 1],
        ["post", customerAddress + "/order", setUpUserHeaders ( withAuthentication, True, authenticationAddress ) , { }, { }               , { }, 400, { "message": "Field requests is missing."                        }, equals, 1],
        ["post", customerAddress + "/order", setUpUserHeaders ( withAuthentication, True, authenticationAddress ) , { }, getOrderError0 ( ), { }, 400, { "message": "Product id is missing for request number 0."       }, equals, 1],
        ["post", customerAddress + "/order", setUpUserHeaders ( withAuthentication, True, authenticationAddress ) , { }, getOrderError1 ( ), { }, 400, { "message": "Product quantity is missing for request number 1." }, equals, 1],
        ["post", customerAddress + "/order", setUpUserHeaders ( withAuthentication, True, authenticationAddress ) , { }, getOrderError2 ( ), { }, 400, { "message": "Invalid product id for request number 0."          }, equals, 1],
        ["post", customerAddress + "/order", setUpUserHeaders ( withAuthentication, True, authenticationAddress ) , { }, getOrderError3 ( ), { }, 400, { "message": "Invalid product id for request number 0."          }, equals, 1],
        ["post", customerAddress + "/order", setUpUserHeaders ( withAuthentication, True, authenticationAddress ) , { }, getOrderError4 ( ), { }, 400, { "message": "Invalid product quantity for request number 0."    }, equals, 1],
        ["post", customerAddress + "/order", setUpUserHeaders ( withAuthentication, True, authenticationAddress ) , { }, getOrderError5 ( ), { }, 400, { "message": "Invalid product quantity for request number 0."    }, equals, 1],
        ["post", customerAddress + "/order", setUpUserHeaders ( withAuthentication, True, authenticationAddress ) , { }, getOrderError6 ( ), { }, 400, { "message": "Invalid product for request number 0."             }, equals, 1],

        # status errors
        ["get", customerAddress + "/search", setUpAuthorizationErrorRequest ( withAuthentication )                , { }, { }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],
        ["get", customerAddress + "/search", setUpAdminHeaders ( withAuthentication, authenticationAddress )      , { }, { }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],
        ["get", customerAddress + "/search", setUpUserHeaders ( withAuthentication, False, authenticationAddress ), { }, { }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],

        # order, status and search
        ["post", customerAddress + "/order", setUpOrderTest ( withAuthentication, authenticationAddress, customerAddress ), { }, getOrder0 ( ), { }, 200, { }, evaluateOrderTest, 2],

        ["get", customerAddress + "/status", setUpUserHeaders ( withAuthentication, True, authenticationAddress ), { }, { }, { }, 200, getOrderStatus0 ( ) , evaluateStatusTest, 7],
        ["get", customerAddress + "/search", setUpUserHeaders ( withAuthentication, True, authenticationAddress ), { }, { }, { }, 200, getSearchResult5 ( ), evaluateSearchTest, 7],

        # update, incomplete order, status and search
        ["post", warehouseAddress + "/update", setUpUpdateTest ( withAuthentication, authenticationAddress, "\n".join ( getData2 ( ) ) ), { }, { }, { }, 200, None, updateTestEquals, 2],

        ["post", customerAddress + "/order", setUpOrderTest ( withAuthentication, authenticationAddress, customerAddress ), { }, getOrder1 ( ), { }, 200, { }, evaluateOrderTest, 2],

        ["get", customerAddress + "/status", setUpUserHeaders ( withAuthentication, True, authenticationAddress ), { }, { }, { }, 200, getOrderStatus1 ( ), evaluateStatusTest, 6],
        ["get", customerAddress + "/search", setUpUserHeaders ( withAuthentication, True, authenticationAddress ), { }, { }, { }, 200, getSearchResult6 ( ), evaluateSearchTest, 6],
    ];

    percentage = runTests ( tests );

    return percentage;
