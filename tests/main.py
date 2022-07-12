import argparse;

from authenticationTests import runAuthenticationTests;
from level0Tests         import runLevel0Tests;
from level1Tests         import runLevel1Tests;
from level2Tests         import runLevel2Tests;
from level3Tests         import runLevel3Tests;

DELIMITER = "=" * 30;

parser = argparse.ArgumentParser (
    description = "IEP store_management grading tests",
    formatter_class = argparse.RawTextHelpFormatter
);

parser.add_argument (
        "--authentication-address",
        help = "Address of the authentication container"
);

parser.add_argument (
        "--jwt-secret",
        help = "JWT secret used to encode JWT tokens"
);

parser.add_argument (
        "--roles-field",
        help = "Name of the field used to store role information in JWT token"
);

parser.add_argument (
        "--customer-role",
        help = "Value which represents the customer role"
);

parser.add_argument (
        "--warehouse-role",
        help = "Value which represents the warehouse manager role"
);

parser.add_argument (
        "--administrator-role",
        help = "Value which represents the administrator role"
);

parser.add_argument (
        "--with-authentication",
        action = "store_true",
        help = "Value which indicates if requests should include authorization header"
);

parser.add_argument (
        "--customer-address",
        help = "Address of the customer container"
);

parser.add_argument (
        "--warehouse-address",
        help = "Address of the warehouse container"
);

parser.add_argument (
        "--administrator-address",
        help = "Address of the administrator container"
);

helpText = """ 
Specifies which tests will be run. Value "authentication" runs test which grade authentication endpoints. Following parameters are required:
    --authentication-address
    --jwt-secret
    --roles-field
    --warehouse-role
    --customer-role
    --admin-role
    
    Example:
    python main.py --type authentication --authentication-address http://127.0.0.1:5000 --jwt-secret JWTSecretDevKey --roles-field roles --administrator-role administrator --customer-role customer --warehouse-role manager

The remainder of the tests are split into levels. Higher level tests will also run lower level tests (if value "level2" is specified, "level0" and "level1" tests will also be included). Following levels are supported:
1) Value "level0" is used for running tests which grade endpoints that update (warehouse container) and search (customer container) products. Following parameters are supported:
    --with-authentication
    --authentication-address
    --warehouse-address
    --customer-address
    
    Parameters --warehouse-address and --customer-address are required. If --with-authentication is present, --authentication-address must also be specified. Example:
    python main.py --type level0 --customer-address http://127.0.0.1:5001 --warehouse-address http://127.0.0.1:5002
    or
    python main.py --type level0 --with-authentication --authentication-address http://127.0.0.1:5000 --customer-address http://127.0.0.1:5001 --warehouse-address http://127.0.0.1:5002
    
2) Value "level1" is used for running tests which grade endpoints that create orders (complete and pending) and retrieve their status. Following parameters are supported:
    --with-authentication
    --authentication-address
    --warehouse-address
    --customer-address
    
    Parameters --warehouse-address and --customer-address are required. If --with-authentication is present, --authentication-address must also be supplied. Example:
    python main.py --type level1 --customer-address http://127.0.0.1:5001 --warehouse-address http://127.0.0.1:5002
    or
    python main.py --type level1 --with-authentication --authentication-address http://127.0.0.1:5000 --customer-address http://127.0.0.1:5001 --warehouse-address http://127.0.0.1:5002
    
3) Value "level2" is used for running tests which grade endpoints that update the status of certain products and orders (FIFO). Following parameters are supported:
    --with-authentication
    --authentication-address
    --warehouse-address
    --customer-address
    
    Parameters --warehouse-address and --customer-address are required. If --with-authentication is present, --authentication-address must also be supplied. Example:
    python main.py --type level2 --customer-address http://127.0.0.1:5001 --warehouse-address http://127.0.0.1:5002
    or
    python main.py --type level2 --with-authentication --authentication-address http://127.0.0.1:5000 --customer-address http://127.0.0.1:5001 --warehouse-address http://127.0.0.1:5002
    
4) Value "level3" is used for running tests which grade endpoints that provide administrators with product and category selling statistics. Following parameters are supported:
    --with-authentication
    --authentication-address
    --warehouse-address
    --customer-address
    --administrator-address
    
    Parameters --warehouse-address, --customer-address and --administrator-address are required. If --with-authentication is present, --authentication-address must also be supplied. Example:
    python main.py --type level3 --customer-address http://127.0.0.1:5001 --warehouse-address http://127.0.0.1:5002 --administrator-address http://127.0.0.1:5003
    or
    python main.py --type level3 --with-authentication --authentication-address http://127.0.0.1:5000 --customer-address http://127.0.0.1:5001 --warehouse-address http://127.0.0.1:5002 --administrator-address http://127.0.0.1:5003
    
Value "all" is used for running all tests. Following parameters are required:
    --authentication-address
    --jwt-secret
    --roles-field
    --warehouse-role
    --customer-role
    --admin-role
    --administrator-address
    --warehouse-address
    --customer-address
    
    Example:
    python main.py --type all --authentication-address http://127.0.0.1:5000 --jwt-secret JWTSecretDevKey --roles-field roles --administrator-role administrator --customer-role customer --warehouse-role manager --customer-address http://127.0.0.1:5001 --warehouse-address http://127.0.0.1:5002 --administrator-address http://127.0.0.1:5003
""";

parser.add_argument (
        "--type",
        required = True,
        choices = ["authentication", "level0", "level1", "level2", "level3", "all"],
        default = "all",
        help = helpText
);


def checkArguments ( arguments, *keys ):
    present = True;
    for key in keys:
        if ( key not in arguments ):
            print ( f"Argument {key} is missing." )

    return present;


AUTHENTICATION = 20.;
LEVEL0         = 10.;
LEVEL1         = 10.;
LEVEL2         = 10.;
LEVEL3         = 10.;

AUTHENTICATION_FACTOR = 0.9;

if (__name__ == "__main__"):
    arguments = parser.parse_args ( );

    total = 0;
    max   = 0;

    if ( ( arguments.type == "all" ) or ( arguments.type == "authentication" ) ):
        correct = checkArguments (
            vars ( arguments ),
            "authentication_address",
            "jwt_secret",
            "roles_field",
            "customer_role",
            "warehouse_role",
            "administrator_role"
        );

        if ( correct ):
            print ( "RUNNING AUTHENTICATION TESTS" );
            print ( DELIMITER );

            percentage = runAuthenticationTests (
                arguments.authentication_address,
                arguments.jwt_secret,
                arguments.roles_field,
                arguments.customer_role,
                arguments.warehouse_role,
                arguments.administrator_role
            );

            authenticationScore = AUTHENTICATION * percentage;

            total += authenticationScore;
            max   += AUTHENTICATION;

            print ( f"AUTHENTICATION = {authenticationScore} / {AUTHENTICATION}" );
            print ( DELIMITER );

    if ( ( arguments.type == "all" ) or ( arguments.type >= "level0" ) ):
        correct = checkArguments (
            vars ( arguments ),
            "warehouse_address",
            "customer_address"
        );

        if ( arguments.with_authentication ):
            correct &= checkArguments (
                vars ( arguments ),
                "authentication_address"
            );

        if ( correct ):
            print ( "RUNNING LEVEL 0 TESTS" );
            print ( DELIMITER );

            percentage = runLevel0Tests (
                arguments.with_authentication,
                arguments.authentication_address,
                arguments.warehouse_address,
                arguments.customer_address
            );

            level0Score = LEVEL0 * percentage;

            if ( not arguments.with_authentication ):
                level0Score *= AUTHENTICATION_FACTOR;

            total += level0Score;
            max   += LEVEL0;

            print ( f"LEVEL 0 = {level0Score} / {LEVEL0}" );
            print ( DELIMITER );

    if ( ( arguments.type == "all" ) or ( arguments.type >= "level1" ) ):
        correct = checkArguments (
            vars ( arguments ),
            "warehouse_address",
            "customer_address"
        );

        if ( arguments.with_authentication ):
            correct &= checkArguments (
                vars ( arguments ),
                "authentication_address"
            );

        if ( correct ):
            print ( "RUNNING LEVEL 1 TESTS" );
            print ( DELIMITER );

            percentage = runLevel1Tests (
                arguments.with_authentication,
                arguments.authentication_address,
                arguments.warehouse_address,
                arguments.customer_address
            );

            level1Score = LEVEL1 * percentage;

            if ( not arguments.with_authentication ):
                level1Score *= AUTHENTICATION_FACTOR;

            total += level1Score;
            max   += LEVEL1;

            print ( f"LEVEL 1 = {level1Score} / {LEVEL1}" );
            print ( DELIMITER );

    if ( ( arguments.type == "all" ) or ( arguments.type >= "level2" ) ):
        correct = checkArguments (
            vars ( arguments ),
            "warehouse_address",
            "customer_address"
        );

        if ( arguments.with_authentication ):
            correct &= checkArguments (
                vars ( arguments ),
                "authentication_address"
            );

        if ( correct ):
            print ( "RUNNING LEVEL 2 TESTS" );
            print ( DELIMITER );

            percentage = runLevel2Tests (
                arguments.with_authentication,
                arguments.authentication_address,
                arguments.warehouse_address,
                arguments.customer_address
            );

            level2Score = LEVEL2 * percentage;

            if ( not arguments.with_authentication ):
                level2Score *= AUTHENTICATION_FACTOR;

            total += level2Score;
            max   += LEVEL2;

            print ( f"LEVEL 2 = {level2Score} / {LEVEL2}" );
            print ( DELIMITER );

    if ( ( arguments.type == "all" ) or ( arguments.type >= "level3" ) ):
        correct = checkArguments (
            vars ( arguments ),
            "warehouse_address",
            "customer_address",
            "administrator_address",
        );

        if ( arguments.with_authentication ):
            correct &= checkArguments (
                vars ( arguments ),
                "authentication_address"
            );

        if ( correct ):
            print ( "RUNNING LEVEL 3 TESTS" );
            print ( DELIMITER );

            percentage = runLevel3Tests (
                arguments.with_authentication,
                arguments.authentication_address,
                arguments.warehouse_address,
                arguments.customer_address,
                arguments.administrator_address
            );

            level3Score = LEVEL3 * percentage;

            if ( not arguments.with_authentication ):
                level3Score *= AUTHENTICATION_FACTOR;

            total += level3Score;
            max   += LEVEL3;

            print ( f"LEVEL 3 = {level3Score} / {LEVEL3}" );
            print ( DELIMITER );

    print ( f"SCORE = {total} / {max}" );
