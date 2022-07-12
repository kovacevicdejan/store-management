from utilities import equals;
from utilities import runTests;
from utilities import setUpAuthorizationErrorRequest;
from utilities import setUpAdminHeaders;
from utilities import setUpUserHeaders;
from utilities import setUpUpdateTest;
from utilities import updateTestEquals;
from utilities import setUpSearchTest;
from utilities import evaluateSearchTest;
from data      import getCsvError0;
from data      import getCsvError1;
from data      import getCsvError2;
from data      import getCsvError3;
from data      import getCsvError4;
from data      import getData0;
from data      import getSearchResult0;
from data      import getData1;
from data      import getSearchParameters1;
from data      import getSearchResult1;
from data      import getSearchParameters2;
from data      import getSearchResult2;
from data      import getSearchParameters3;
from data      import getSearchResult3;
from data      import getSearchParameters4;
from data      import getSearchResult4;

def runLevel0Tests ( withAuthentication, authenticationAddress, warehouseAddress, customerAddress ):

    tests = [
        # update errors
        ["post", warehouseAddress + "/update", setUpAuthorizationErrorRequest ( withAuthentication )                          , { }, { }, { }, 401, { "msg": "Missing Authorization Header"              }, equals, 1],
        ["post", warehouseAddress + "/update", setUpAdminHeaders ( withAuthentication, authenticationAddress )                , { }, { }, { }, 401, { "msg": "Missing Authorization Header"              }, equals, 1],
        ["post", warehouseAddress + "/update", setUpUserHeaders ( withAuthentication, True, authenticationAddress )           , { }, { }, { }, 401, { "msg": "Missing Authorization Header"              }, equals, 1],
        ["post", warehouseAddress + "/update", setUpUserHeaders ( withAuthentication, False, authenticationAddress )          , { }, { }, { }, 400, { "message": "Field file is missing."                }, equals, 1],
        ["post", warehouseAddress + "/update", setUpUpdateTest ( withAuthentication, authenticationAddress, getCsvError0 ( ) ), { }, { }, { }, 400, { "message": "Incorrect number of values on line 2." }, equals, 1],
        ["post", warehouseAddress + "/update", setUpUpdateTest ( withAuthentication, authenticationAddress, getCsvError1 ( ) ), { }, { }, { }, 400, { "message": "Incorrect quantity on line 3."         }, equals, 1],
        ["post", warehouseAddress + "/update", setUpUpdateTest ( withAuthentication, authenticationAddress, getCsvError2 ( ) ), { }, { }, { }, 400, { "message": "Incorrect quantity on line 3."         }, equals, 1],
        ["post", warehouseAddress + "/update", setUpUpdateTest ( withAuthentication, authenticationAddress, getCsvError3 ( ) ), { }, { }, { }, 400, { "message": "Incorrect price on line 1."            }, equals, 1],
        ["post", warehouseAddress + "/update", setUpUpdateTest ( withAuthentication, authenticationAddress, getCsvError4 ( ) ), { }, { }, { }, 400, { "message": "Incorrect price on line 1."            }, equals, 1],

        # search errors
        ["get", customerAddress + "/search", setUpAuthorizationErrorRequest ( withAuthentication )                , { }, { }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],
        ["get", customerAddress + "/search", setUpAdminHeaders ( withAuthentication, authenticationAddress )      , { }, { }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],
        ["get", customerAddress + "/search", setUpUserHeaders ( withAuthentication, False, authenticationAddress ), { }, { }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],

        # valid update and empty search
        ["post", warehouseAddress + "/update", setUpUpdateTest ( withAuthentication, authenticationAddress, getData0 ( ) ), { }, { }, { }, 200, None, updateTestEquals, 1],

        ["get", customerAddress + "/search", setUpUserHeaders ( withAuthentication, True, authenticationAddress ), { }, { }, { }, 200, getSearchResult0 ( ) , evaluateSearchTest, 7],

        # invalid update (different categories) and empty search
        ["post", warehouseAddress + "/update", setUpUpdateTest ( withAuthentication, authenticationAddress, getData1 ( ) ), { }, { }, { }, 200, None, updateTestEquals, 1],

        ["get", customerAddress + "/search", setUpUserHeaders ( withAuthentication, True, authenticationAddress ), { }, { }, { }, 200, getSearchResult0 ( ), evaluateSearchTest, 7],

        # parameterized search
        ["get", customerAddress + "/search", setUpSearchTest ( withAuthentication, authenticationAddress, getSearchParameters1 ( ) ), { }, { }, { }, 200, getSearchResult1 ( ), evaluateSearchTest, 3],
        ["get", customerAddress + "/search", setUpSearchTest ( withAuthentication, authenticationAddress, getSearchParameters2 ( ) ), { }, { }, { }, 200, getSearchResult2 ( ), evaluateSearchTest, 3],
        ["get", customerAddress + "/search", setUpSearchTest ( withAuthentication, authenticationAddress, getSearchParameters3 ( ) ), { }, { }, { }, 200, getSearchResult3 ( ), evaluateSearchTest, 3],
        ["get", customerAddress + "/search", setUpSearchTest ( withAuthentication, authenticationAddress, getSearchParameters4 ( ) ), { }, { }, { }, 200, getSearchResult4 ( ), evaluateSearchTest, 3],
    ];

    percentage = runTests ( tests );

    return percentage;
