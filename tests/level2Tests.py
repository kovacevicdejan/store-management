from utilities import runTests;
from utilities import setUpUserHeaders;
from utilities import evaluateSearchTest;
from utilities import setUpOrderTest;
from utilities import evaluateStatusTest;
from utilities import evaluateOrderTest;
from utilities import setUpUpdateTest;
from utilities import updateTestEquals;
from data      import getOrder2;
from data      import getOrderStatus2;
from data      import getSearchResult7;
from data      import getData3;
from data      import getOrderStatus3;
from data      import getSearchResult8;
from data      import getData4;
from data      import getOrderStatus4;
from data      import getSearchResult9;

def runLevel2Tests ( withAuthentication, authenticationAddress, warehouseAddress, customerAddress ):

    tests = [
        # order, status and search
        ["post", customerAddress + "/order", setUpOrderTest ( withAuthentication, authenticationAddress, customerAddress ), { }, getOrder2 ( ), { }, 200, { }, evaluateOrderTest, 1],

        ["get" , customerAddress + "/status", setUpUserHeaders ( withAuthentication, True, authenticationAddress ), { }, { }, { }, 200, getOrderStatus2 ( ) , evaluateStatusTest, 5],
        ["get" , customerAddress + "/search", setUpUserHeaders ( withAuthentication, True, authenticationAddress ), { }, { }, { }, 200, getSearchResult7 ( ), evaluateSearchTest, 5],

        # update, status and search
        ["post", warehouseAddress + "/update", setUpUpdateTest ( withAuthentication, authenticationAddress, getData3 ( ) ), { }, { }, { }, 200, None, updateTestEquals, 1],

        ["get", customerAddress + "/status", setUpUserHeaders ( withAuthentication, True, authenticationAddress ), { }, { }, { }, 200, getOrderStatus3 ( ) , evaluateStatusTest, 5],
        ["get", customerAddress + "/search", setUpUserHeaders ( withAuthentication, True, authenticationAddress ), { }, { }, { }, 200, getSearchResult8 ( ), evaluateSearchTest, 5],

        # update, status and search
        ["post", warehouseAddress + "/update", setUpUpdateTest ( withAuthentication, authenticationAddress, getData4 ( ) ), { }, { }, { }, 200, None, updateTestEquals, 1],

        ["get", customerAddress + "/status", setUpUserHeaders ( withAuthentication, True, authenticationAddress ), { }, { }, { }, 200, getOrderStatus4 ( ) , evaluateStatusTest, 5],
        ["get", customerAddress + "/search", setUpUserHeaders ( withAuthentication, True, authenticationAddress ), { }, { }, { }, 200, getSearchResult9 ( ), evaluateSearchTest, 5],
    ];

    percentage = runTests ( tests );

    return percentage;
