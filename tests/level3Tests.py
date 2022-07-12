from utilities import equals;
from utilities import runTests;
from utilities import setUpAuthorizationErrorRequest;
from utilities import setUpAdminHeaders;
from utilities import setUpUserHeaders;
from utilities import evaluateProductStatisticsTest;
from utilities import evaluateCategoryStatisticsTest;
from utilities import evaluateSearchTest;
from utilities import setUpOrderTest;
from utilities import evaluateOrderTest;
from utilities import setUpUpdateTest;
from utilities import updateTestEquals;
from data      import getOrder3;
from data      import getOrder4;
from data      import getData5;
from data      import getProductStatistics0;
from data      import getCategoryStatistics0;
from data      import getProductStatistics1;
from data      import getCategoryStatistics1;
from data      import getProductStatistics2;
from data      import getCategoryStatistics2;
from data      import getProductStatistics3;
from data      import getSearchResult10;

def runLevel3Tests ( withAuthentication, authenticationAddress, warehouseAddress, customerAddress, administratorAddress ):

    tests = [
        # products statistics error
        ["get", administratorAddress + "/productStatistics", setUpAuthorizationErrorRequest ( withAuthentication )                , { }, { }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],
        ["get", administratorAddress + "/productStatistics", setUpUserHeaders ( withAuthentication, True, authenticationAddress ) , { }, { }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],
        ["get", administratorAddress + "/productStatistics", setUpUserHeaders ( withAuthentication, False, authenticationAddress ), { }, { }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],

        # category statistics error
        ["get", administratorAddress + "/categoryStatistics", setUpAuthorizationErrorRequest ( withAuthentication )                , { }, { }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],
        ["get", administratorAddress + "/categoryStatistics", setUpUserHeaders ( withAuthentication, True, authenticationAddress ) , { }, { }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],
        ["get", administratorAddress + "/categoryStatistics", setUpUserHeaders ( withAuthentication, False, authenticationAddress ), { }, { }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],

        # statistics 0
        ["get", administratorAddress + "/productStatistics" , setUpAdminHeaders ( withAuthentication, authenticationAddress ), { }, { }, { }, 200, getProductStatistics0 ( ) , evaluateProductStatisticsTest , 4],
        ["get", administratorAddress + "/categoryStatistics", setUpAdminHeaders ( withAuthentication, authenticationAddress ), { }, { }, { }, 200, getCategoryStatistics0 ( ), evaluateCategoryStatisticsTest, 4],

        # statistics 1
        ["post", customerAddress + "/order", setUpOrderTest ( withAuthentication, authenticationAddress, customerAddress ), { }, getOrder3 ( ), { }, 200, { }, evaluateOrderTest, 1],

        ["get", administratorAddress + "/productStatistics", setUpAdminHeaders ( withAuthentication, authenticationAddress ), { }, { }, { }, 200, getProductStatistics1 ( ), evaluateProductStatisticsTest, 4.5],
        ["get", administratorAddress + "/categoryStatistics", setUpAdminHeaders ( withAuthentication, authenticationAddress ), { }, { }, { }, 200, getCategoryStatistics1 ( ), evaluateCategoryStatisticsTest, 4.5],

        # statistics 2
        ["post", customerAddress + "/order", setUpOrderTest ( withAuthentication, authenticationAddress, customerAddress ), { }, getOrder4 ( ), { }, 200, { }, evaluateOrderTest, 1],

        ["get", administratorAddress + "/productStatistics", setUpAdminHeaders ( withAuthentication, authenticationAddress ), { }, { }, { }, 200, getProductStatistics2 ( ), evaluateProductStatisticsTest, 4.5],
        ["get", administratorAddress + "/categoryStatistics", setUpAdminHeaders ( withAuthentication, authenticationAddress ), { }, { }, { }, 200, getCategoryStatistics2 ( ), evaluateCategoryStatisticsTest, 4.5],

        # statistics 3
        ["post", warehouseAddress + "/update", setUpUpdateTest ( withAuthentication, authenticationAddress, getData5 ( ) ), { }, { }, { }, 200, None, updateTestEquals, 1],

        ["get", administratorAddress + "/productStatistics", setUpAdminHeaders ( withAuthentication, authenticationAddress ), { }, { }, { }, 200, getProductStatistics3 ( ), evaluateProductStatisticsTest, 8],

        ["get", customerAddress + "/search", setUpUserHeaders ( withAuthentication, True, authenticationAddress ), { }, { }, { }, 200, getSearchResult10 ( ), evaluateSearchTest, 3],
    ];

    percentage = runTests ( tests );

    return percentage;
