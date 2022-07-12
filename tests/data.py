# AUTHENTICATION DATA
users = {
    True : {
        "forename"  : "John",
        "surname"   : "Doe",
        "email"     : "john@gmail.com",
        "password"  : "aA123456",
        "isCustomer": True,
    },
    False: {
        "forename"  : "Jane",
        "surname"   : "Doe",
        "email"     : "jane@gmail.com",
        "password"  : "aA123456",
        "isCustomer": False,
    }
};

isRegistered = {
    True : False,
    False: False
};


def getUser ( isCustomer ):
    global users;
    return users[isCustomer];


def getIsUserRegistered ( isCustomer ):
    global isRegistered;
    return isRegistered[isCustomer];


def setIsUserRegistered ( isCustomer, value ):
    global isRegistered;
    isRegistered[isCustomer] = value;


# LEVEL 0 DATA
getCsvError0 = lambda: "\n".join ( [
    "Category0,Product0,2,27.34",
    "Category0,Product1,5,41.44",
    "Category1|Category2,Product2",
    "Category2,Product3,4,37.36",
    "Category6,Product4,4,13.64",
    "Category3,Product5,4,26.33",
    "Category5,Product6,3,20.09",
    "Category4,Product7,5,47.75",
    "Category4,Product8,2,15.47",
    "Category0,Product9,4,41.3",
    "Category0|Category1|Category2,Product10,5,17.98",
] );

getCsvError1 = lambda: "\n".join ( [
    "Category0,Product0,2,27.34",
    "Category0,Product1,5,41.44",
    "Category1|Category2,Product2,5,29.89",
    "Category2,Product3,x,37.36",
    "Category6,Product4,4,13.64",
    "Category3,Product5,4,26.33",
    "Category5,Product6,3,20.09",
    "Category4,Product7,5,47.75",
    "Category4,Product8,2,15.47",
    "Category0,Product9,4,41.3",
    "Category0|Category1|Category2,Product10,5,17.98",
] );

getCsvError2 = lambda: "\n".join ( [
    "Category0,Product0,2,27.34",
    "Category0,Product1,5,41.44",
    "Category1|Category2,Product2,5,29.89",
    "Category2,Product3,-1,37.36",
    "Category6,Product4,4,13.64",
    "Category3,Product5,4,26.33",
    "Category5,Product6,3,20.09",
    "Category4,Product7,5,47.75",
    "Category4,Product8,2,15.47",
    "Category0,Product9,4,41.3",
    "Category0|Category1|Category2,Product10,5,17.98",
] );

getCsvError3 = lambda: "\n".join ( [
    "Category0,Product0,2,27.34",
    "Category0,Product1,5,x",
    "Category1|Category2,Product2,5,29.89",
    "Category2,Product3,4,37.36",
    "Category6,Product4,4,13.64",
    "Category3,Product5,4,26.33",
    "Category5,Product6,3,20.09",
    "Category4,Product7,5,47.75",
    "Category4,Product8,2,15.47",
    "Category0,Product9,4,41.3",
    "Category0|Category1|Category2,Product10,5,17.98",
] );

getCsvError4 = lambda: "\n".join ( [
    "Category0,Product0,2,27.34",
    "Category0,Product1,5,-1.2",
    "Category1|Category2,Product2,5,29.89",
    "Category2,Product3,4,37.36",
    "Category6,Product4,4,13.64",
    "Category3,Product5,4,26.33",
    "Category5,Product6,3,20.09",
    "Category4,Product7,5,47.75",
    "Category4,Product8,2,15.47",
    "Category0,Product9,4,41.3",
    "Category0|Category1|Category2,Product10,5,17.98",
] );


getData0 = lambda: "\n".join ( [
    "Category0,Product0,2,27.34",
    "Category0,Product1,5,41.44",
    "Category1|Category2,Product2,5,29.89",
    "Category2,Product3,4,37.36",
    "Category6,Product4,4,13.64",
    "Category3,Product5,4,26.33",
    "Category5,Product6,3,20.09",
    "Category4,Product7,5,47.75",
    "Category4,Product8,2,15.47",
    "Category0,Product9,4,41.3",
    "Category0|Category1|Category2,Product10,5,17.98",
] );

getSearchResult0 = lambda: {
    "categories": [
        "Category0",
        "Category2",
        "Category1",
        "Category6",
        "Category3",
        "Category5",
        "Category4"
    ],
    "products"  : [
        {
            "categories": [
                "Category0"
            ],
            "id"        : 1,
            "name"      : "Product0",
            "price"     : 27.34,
            "quantity"  : 2
        },
        {
            "categories": [
                "Category0"
            ],
            "id"        : 2,
            "name"      : "Product1",
            "price"     : 41.44,
            "quantity"  : 5
        },
        {
            "categories": [
                "Category1",
                "Category2"
            ],
            "id"        : 3,
            "name"      : "Product2",
            "price"     : 29.89,
            "quantity"  : 5
        },
        {
            "categories": [
                "Category2"
            ],
            "id"        : 4,
            "name"      : "Product3",
            "price"     : 37.36,
            "quantity"  : 4
        },
        {
            "categories": [
                "Category6"
            ],
            "id"        : 5,
            "name"      : "Product4",
            "price"     : 13.64,
            "quantity"  : 4
        },
        {
            "categories": [
                "Category3"
            ],
            "id"        : 6,
            "name"      : "Product5",
            "price"     : 26.33,
            "quantity"  : 4
        },
        {
            "categories": [
                "Category5"
            ],
            "id"        : 7,
            "name"      : "Product6",
            "price"     : 20.09,
            "quantity"  : 3
        },
        {
            "categories": [
                "Category4"
            ],
            "id"        : 8,
            "name"      : "Product7",
            "price"     : 47.75,
            "quantity"  : 5
        },
        {
            "categories": [
                "Category4"
            ],
            "id"        : 9,
            "name"      : "Product8",
            "price"     : 15.47,
            "quantity"  : 2
        },
        {
            "categories": [
                "Category0"
            ],
            "id"        : 10,
            "name"      : "Product9",
            "price"     : 41.3,
            "quantity"  : 4
        },
        {
            "categories": [
                "Category0",
                "Category1",
                "Category2"
            ],
            "id"        : 11,
            "name"      : "Product10",
            "price"     : 17.98,
            "quantity"  : 5
        }
    ]
};

getData1 = lambda: "\n".join ( [
    "Category1,Product0,2,17.34",
    "Category1,Product1,4,51.44",
    "Category2|Category5,Product2,7,9.89",
    "Category3,Product3,5,7.36",
] );

getSearchParameters1 = lambda: "name=0";
getSearchResult1 = lambda: {
    "categories": [
        "Category0",
        "Category2",
        "Category1"
    ],
    "products"  : [
        {
            "categories": [
                "Category0"
            ],
            "id"        : 1,
            "name"      : "Product0",
            "price"     : 27.34,
            "quantity"  : 2
        },
        {
            "categories": [
                "Category0",
                "Category1",
                "Category2"
            ],
            "id"        : 11,
            "name"      : "Product10",
            "price"     : 17.98,
            "quantity"  : 5
        }
    ]
};

getSearchParameters2 = lambda: "name=2";
getSearchResult2 = lambda: {
    "categories": [
        "Category2",
        "Category1"
    ],
    "products"  : [
        {
            "categories": [
                "Category1",
                "Category2"
            ],
            "id"        : 3,
            "name"      : "Product2",
            "price"     : 29.89,
            "quantity"  : 5
        }
    ]
};

getSearchParameters3 = lambda: "category=5";
getSearchResult3 = lambda: {
    "categories": [
        "Category5"
    ],
    "products"  : [
        {
            "categories": [
                "Category5"
            ],
            "id"        : 7,
            "name"      : "Product6",
            "price"     : 20.09,
            "quantity"  : 3
        }
    ]
};

getSearchParameters4 = lambda: "category=5,name=0";
getSearchResult4 = lambda: {
    "categories": [],
    "products"  : []
};

# LEVEL 1 DATA
getOrderError0 = lambda: {
    "requests": [
        { }
    ]
};

getOrderError1 = lambda: {
    "requests": [
        {
            "id"      : 1,
            "quantity": 1
        },
        {
            "id": 1
        }
    ]
};

getOrderError2 = lambda: {
    "requests": [
        {
            "id"      : "x",
            "quantity": 1
        }
    ]
};

getOrderError3 = lambda : {
    "requests": [
        {
            "id"      : -1,
            "quantity": 1
        }
    ]
};

getOrderError4 = lambda : {
    "requests": [
        {
            "id"      : 1,
            "quantity": "x"
        }
    ]
};

getOrderError5 = lambda : {
    "requests": [
        {
            "id"      : 1,
            "quantity": -1
        }
    ]
};

getOrderError6 = lambda : {
    "requests": [
        {
            "id"      : 10000000000,
            "quantity": 1
        }
    ]
};

getOrder0 = lambda : {
    "requests": [
        {
            "id"      : "Product0",
            "quantity": 2
        },
        {
            "id"      : "Product1",
            "quantity": 3
        }
    ]
};

getOrderStatus0 = lambda: {
    "orders": [
        {
            "products" : [
                {
                    "categories": [
                        "Category0"
                    ],
                    "name"      : "Product0",
                    "price"     : 27.34,
                    "received"  : 2,
                    "requested" : 2
                },
                {
                    "categories": [
                        "Category0"
                    ],
                    "name"      : "Product1",
                    "price"     : 41.44,
                    "received"  : 3,
                    "requested" : 3
                }
            ],
            "price"    : 179.0,
            "status"   : "COMPLETE",
            "timestamp": "2022-05-22 20:32:17"
        }
    ]
};

getSearchResult5 = lambda: {
    "categories": [
        "Category0",
        "Category2",
        "Category1",
        "Category6",
        "Category3",
        "Category5",
        "Category4"
    ],
    "products"  : [
        {
            "categories": [
                "Category0"
            ],
            "id"        : 1,
            "name"      : "Product0",
            "price"     : 27.34,
            "quantity"  : 0
        },
        {
            "categories": [
                "Category0"
            ],
            "id"        : 2,
            "name"      : "Product1",
            "price"     : 41.44,
            "quantity"  : 2
        },
        {
            "categories": [
                "Category1",
                "Category2"
            ],
            "id"        : 3,
            "name"      : "Product2",
            "price"     : 29.89,
            "quantity"  : 5
        },
        {
            "categories": [
                "Category2"
            ],
            "id"        : 4,
            "name"      : "Product3",
            "price"     : 37.36,
            "quantity"  : 4
        },
        {
            "categories": [
                "Category6"
            ],
            "id"        : 5,
            "name"      : "Product4",
            "price"     : 13.64,
            "quantity"  : 4
        },
        {
            "categories": [
                "Category3"
            ],
            "id"        : 6,
            "name"      : "Product5",
            "price"     : 26.33,
            "quantity"  : 4
        },
        {
            "categories": [
                "Category5"
            ],
            "id"        : 7,
            "name"      : "Product6",
            "price"     : 20.09,
            "quantity"  : 3
        },
        {
            "categories": [
                "Category4"
            ],
            "id"        : 8,
            "name"      : "Product7",
            "price"     : 47.75,
            "quantity"  : 5
        },
        {
            "categories": [
                "Category4"
            ],
            "id"        : 9,
            "name"      : "Product8",
            "price"     : 15.47,
            "quantity"  : 2
        },
        {
            "categories": [
                "Category0"
            ],
            "id"        : 10,
            "name"      : "Product9",
            "price"     : 41.3,
            "quantity"  : 4
        },
        {
            "categories": [
                "Category0",
                "Category1",
                "Category2"
            ],
            "id"        : 11,
            "name"      : "Product10",
            "price"     : 17.98,
            "quantity"  : 5
        }
    ]
};

getData2 = lambda: {
    "Category0,Product1,5,20.44"
};

getOrder1 = lambda: {
    "requests": [
        {
            "id"      : "Product0",
            "quantity": 2
        },
        {
            "id"      : "Product1",
            "quantity": 8
        }
    ]
};

getOrderStatus1 = lambda: {
    "orders": [
        {
            "products" : [
                {
                    "categories": [
                        "Category0"
                    ],
                    "name"      : "Product0",
                    "price"     : 27.34,
                    "received"  : 2,
                    "requested" : 2
                },
                {
                    "categories": [
                        "Category0"
                    ],
                    "name"      : "Product1",
                    "price"     : 41.44,
                    "received"  : 3,
                    "requested" : 3
                }
            ],
            "price"    : 179.0,
            "status"   : "COMPLETE",
            "timestamp": "2022-05-22 20:32:17"
        },
        {
            "products" : [
                {
                    "categories": [
                        "Category0"
                    ],
                    "name"      : "Product0",
                    "price"     : 27.34,
                    "received"  : 0,
                    "requested" : 2
                },
                {
                    "categories": [
                        "Category0"
                    ],
                    "name"      : "Product1",
                    "price"     : 26.44,
                    "received"  : 7,
                    "requested" : 8
                }
            ],
            "price"    : 266.2,
            "status"   : "PENDING",
            "timestamp": "2022-05-22 21:41:48"
        }
    ]
};

getSearchResult6 = lambda: {
    "categories": [
        "Category0",
        "Category1",
        "Category2",
        "Category6",
        "Category3",
        "Category5",
        "Category4"
    ],
    "products"  : [
        {
            "categories": [
                "Category0"
            ],
            "id"        : 1,
            "name"      : "Product0",
            "price"     : 27.34,
            "quantity"  : 0
        },
        {
            "categories": [
                "Category0"
            ],
            "id"        : 2,
            "name"      : "Product1",
            "price"     : 26.44,
            "quantity"  : 0
        },
        {
            "categories": [
                "Category0"
            ],
            "id"        : 10,
            "name"      : "Product9",
            "price"     : 41.3,
            "quantity"  : 4
        },
        {
            "categories": [
                "Category0",
                "Category1",
                "Category2"
            ],
            "id"        : 11,
            "name"      : "Product10",
            "price"     : 17.98,
            "quantity"  : 5
        },
        {
            "categories": [
                "Category1",
                "Category2"
            ],
            "id"        : 3,
            "name"      : "Product2",
            "price"     : 29.89,
            "quantity"  : 5
        },
        {
            "categories": [
                "Category2"
            ],
            "id"        : 4,
            "name"      : "Product3",
            "price"     : 37.36,
            "quantity"  : 4
        },
        {
            "categories": [
                "Category6"
            ],
            "id"        : 5,
            "name"      : "Product4",
            "price"     : 13.64,
            "quantity"  : 4
        },
        {
            "categories": [
                "Category3"
            ],
            "id"        : 6,
            "name"      : "Product5",
            "price"     : 26.33,
            "quantity"  : 4
        },
        {
            "categories": [
                "Category5"
            ],
            "id"        : 7,
            "name"      : "Product6",
            "price"     : 20.09,
            "quantity"  : 3
        },
        {
            "categories": [
                "Category4"
            ],
            "id"        : 8,
            "name"      : "Product7",
            "price"     : 47.75,
            "quantity"  : 5
        },
        {
            "categories": [
                "Category4"
            ],
            "id"        : 9,
            "name"      : "Product8",
            "price"     : 15.47,
            "quantity"  : 2
        }
    ]
};

# LEVEL 2 DATA
getOrder2 = lambda: {
    "requests": [
        {
            "id"      : "Product9",
            "quantity": 4
        },
        {
            "id"      : "Product1",
            "quantity": 1
        }
    ]
};

getOrderStatus2 = lambda : {
    "orders": [
        {
            "products": [
                {
                    "categories": [
                        "Category0"
                    ],
                    "name": "Product0",
                    "price": 27.34,
                    "received": 2,
                    "requested": 2
                },
                {
                    "categories": [
                        "Category0"
                    ],
                    "name": "Product1",
                    "price": 41.44,
                    "received": 3,
                    "requested": 3
                }
            ],
            "price": 179.0,
            "status": "COMPLETE",
            "timestamp": "2022-05-22 20:32:17"
        },
        {
            "products": [
                {
                    "categories": [
                        "Category0"
                    ],
                    "name": "Product0",
                    "price": 27.34,
                    "received": 0,
                    "requested": 2
                },
                {
                    "categories": [
                        "Category0"
                    ],
                    "name": "Product1",
                    "price": 26.44,
                    "received": 7,
                    "requested": 8
                }
            ],
            "price": 266.2,
            "status": "PENDING",
            "timestamp": "2022-05-22 21:41:48"
        },
        {
            "products": [
                {
                    "categories": [
                        "Category0"
                    ],
                    "name": "Product9",
                    "price": 41.3,
                    "received": 4,
                    "requested": 4
                },
                {
                    "categories": [
                        "Category0"
                    ],
                    "name": "Product1",
                    "price": 26.44,
                    "received": 0,
                    "requested": 1
                }
            ],
            "price": 191.64,
            "status": "PENDING",
            "timestamp": "2022-05-22 21:55:53"
        }
    ]
};

getSearchResult7 = lambda : {
    "categories": [
        "Category0",
        "Category2",
        "Category1",
        "Category6",
        "Category3",
        "Category5",
        "Category4"
    ],
    "products": [
        {
            "categories": [
                "Category0"
            ],
            "id": 1,
            "name": "Product0",
            "price": 27.34,
            "quantity": 0
        },
        {
            "categories": [
                "Category0"
            ],
            "id": 2,
            "name": "Product1",
            "price": 26.44,
            "quantity": 0
        },
        {
            "categories": [
                "Category1",
                "Category2"
            ],
            "id": 3,
            "name": "Product2",
            "price": 29.89,
            "quantity": 5
        },
        {
            "categories": [
                "Category2"
            ],
            "id": 4,
            "name": "Product3",
            "price": 37.36,
            "quantity": 4
        },
        {
            "categories": [
                "Category6"
            ],
            "id": 5,
            "name": "Product4",
            "price": 13.64,
            "quantity": 4
        },
        {
            "categories": [
                "Category3"
            ],
            "id": 6,
            "name": "Product5",
            "price": 26.33,
            "quantity": 4
        },
        {
            "categories": [
                "Category5"
            ],
            "id": 7,
            "name": "Product6",
            "price": 20.09,
            "quantity": 3
        },
        {
            "categories": [
                "Category4"
            ],
            "id": 8,
            "name": "Product7",
            "price": 47.75,
            "quantity": 5
        },
        {
            "categories": [
                "Category4"
            ],
            "id": 9,
            "name": "Product8",
            "price": 15.47,
            "quantity": 2
        },
        {
            "categories": [
                "Category0"
            ],
            "id": 10,
            "name": "Product9",
            "price": 41.3,
            "quantity": 0
        },
        {
            "categories": [
                "Category0",
                "Category1",
                "Category2"
            ],
            "id": 11,
            "name": "Product10",
            "price": 17.98,
            "quantity": 5
        }
    ]
};

getData3 = lambda : "\n".join ( [
    "Category0,Product1,1,20.44"
] );

getOrderStatus3 = lambda : {
    "orders": [
        {
            "products": [
                {
                    "categories": [
                        "Category0"
                    ],
                    "name": "Product0",
                    "price": 27.34,
                    "received": 2,
                    "requested": 2
                },
                {
                    "categories": [
                        "Category0"
                    ],
                    "name": "Product1",
                    "price": 41.44,
                    "received": 3,
                    "requested": 3
                }
            ],
            "price": 179.0,
            "status": "COMPLETE",
            "timestamp": "2022-05-22 20:32:17"
        },
        {
            "products": [
                {
                    "categories": [
                        "Category0"
                    ],
                    "name": "Product0",
                    "price": 27.34,
                    "received": 0,
                    "requested": 2
                },
                {
                    "categories": [
                        "Category0"
                    ],
                    "name": "Product1",
                    "price": 26.44,
                    "received": 8,
                    "requested": 8
                }
            ],
            "price": 266.2,
            "status": "PENDING",
            "timestamp": "2022-05-22 21:41:48"
        },
        {
            "products": [
                {
                    "categories": [
                        "Category0"
                    ],
                    "name": "Product9",
                    "price": 41.3,
                    "received": 4,
                    "requested": 4
                },
                {
                    "categories": [
                        "Category0"
                    ],
                    "name": "Product1",
                    "price": 26.44,
                    "received": 0,
                    "requested": 1
                }
            ],
            "price": 191.64,
            "status": "PENDING",
            "timestamp": "2022-05-22 21:55:53"
        }
    ]
};

getSearchResult8 = lambda : {
    "categories": [
        "Category0",
        "Category2",
        "Category1",
        "Category6",
        "Category3",
        "Category5",
        "Category4"
    ],
    "products": [
        {
            "categories": [
                "Category0"
            ],
            "id": 1,
            "name": "Product0",
            "price": 27.34,
            "quantity": 0
        },
        {
            "categories": [
                "Category0"
            ],
            "id": 2,
            "name": "Product1",
            "price": 20.44,
            "quantity": 0
        },
        {
            "categories": [
                "Category1",
                "Category2"
            ],
            "id": 3,
            "name": "Product2",
            "price": 29.89,
            "quantity": 5
        },
        {
            "categories": [
                "Category2"
            ],
            "id": 4,
            "name": "Product3",
            "price": 37.36,
            "quantity": 4
        },
        {
            "categories": [
                "Category6"
            ],
            "id": 5,
            "name": "Product4",
            "price": 13.64,
            "quantity": 4
        },
        {
            "categories": [
                "Category3"
            ],
            "id": 6,
            "name": "Product5",
            "price": 26.33,
            "quantity": 4
        },
        {
            "categories": [
                "Category5"
            ],
            "id": 7,
            "name": "Product6",
            "price": 20.09,
            "quantity": 3
        },
        {
            "categories": [
                "Category4"
            ],
            "id": 8,
            "name": "Product7",
            "price": 47.75,
            "quantity": 5
        },
        {
            "categories": [
                "Category4"
            ],
            "id": 9,
            "name": "Product8",
            "price": 15.47,
            "quantity": 2
        },
        {
            "categories": [
                "Category0"
            ],
            "id": 10,
            "name": "Product9",
            "price": 41.3,
            "quantity": 0
        },
        {
            "categories": [
                "Category0",
                "Category1",
                "Category2"
            ],
            "id": 11,
            "name": "Product10",
            "price": 17.98,
            "quantity": 5
        }
    ]
};

getData4 = lambda : "\n".join ( [
    "Category0,Product0,2,20.44",
    "Category0,Product1,1,30.44",
] );

getOrderStatus4 = lambda : {
    "orders": [
        {
            "products": [
                {
                    "categories": [
                        "Category0"
                    ],
                    "name": "Product0",
                    "price": 27.34,
                    "received": 2,
                    "requested": 2
                },
                {
                    "categories": [
                        "Category0"
                    ],
                    "name": "Product1",
                    "price": 41.44,
                    "received": 3,
                    "requested": 3
                }
            ],
            "price": 179.0,
            "status": "COMPLETE",
            "timestamp": "2022-05-22 20:32:17"
        },
        {
            "products": [
                {
                    "categories": [
                        "Category0"
                    ],
                    "name": "Product0",
                    "price": 27.34,
                    "received": 2,
                    "requested": 2
                },
                {
                    "categories": [
                        "Category0"
                    ],
                    "name": "Product1",
                    "price": 26.44,
                    "received": 8,
                    "requested": 8
                }
            ],
            "price": 266.2,
            "status": "COMPLETE",
            "timestamp": "2022-05-22 21:41:48"
        },
        {
            "products": [
                {
                    "categories": [
                        "Category0"
                    ],
                    "name": "Product9",
                    "price": 41.3,
                    "received": 4,
                    "requested": 4
                },
                {
                    "categories": [
                        "Category0"
                    ],
                    "name": "Product1",
                    "price": 26.44,
                    "received": 1,
                    "requested": 1
                }
            ],
            "price": 191.64,
            "status": "COMPLETE",
            "timestamp": "2022-05-22 21:55:53"
        }
    ]
};

getSearchResult9 = lambda : {
    "categories": [
        "Category0",
        "Category2",
        "Category1",
        "Category6",
        "Category3",
        "Category5",
        "Category4"
    ],
    "products": [
        {
            "categories": [
                "Category0"
            ],
            "id": 1,
            "name": "Product0",
            "price": 20.44,
            "quantity": 0
        },
        {
            "categories": [
                "Category0"
            ],
            "id": 2,
            "name": "Product1",
            "price": 30.44,
            "quantity": 0
        },
        {
            "categories": [
                "Category1",
                "Category2"
            ],
            "id": 3,
            "name": "Product2",
            "price": 29.89,
            "quantity": 5
        },
        {
            "categories": [
                "Category2"
            ],
            "id": 4,
            "name": "Product3",
            "price": 37.36,
            "quantity": 4
        },
        {
            "categories": [
                "Category6"
            ],
            "id": 5,
            "name": "Product4",
            "price": 13.64,
            "quantity": 4
        },
        {
            "categories": [
                "Category3"
            ],
            "id": 6,
            "name": "Product5",
            "price": 26.33,
            "quantity": 4
        },
        {
            "categories": [
                "Category5"
            ],
            "id": 7,
            "name": "Product6",
            "price": 20.09,
            "quantity": 3
        },
        {
            "categories": [
                "Category4"
            ],
            "id": 8,
            "name": "Product7",
            "price": 47.75,
            "quantity": 5
        },
        {
            "categories": [
                "Category4"
            ],
            "id": 9,
            "name": "Product8",
            "price": 15.47,
            "quantity": 2
        },
        {
            "categories": [
                "Category0"
            ],
            "id": 10,
            "name": "Product9",
            "price": 41.3,
            "quantity": 0
        },
        {
            "categories": [
                "Category0",
                "Category1",
                "Category2"
            ],
            "id": 11,
            "name": "Product10",
            "price": 17.98,
            "quantity": 5
        }
    ]
};

# LEVEL 3 DATA
getProductStatistics0 = lambda : {
    "statistics": [
        {
            "name": "Product0",
            "sold": 4,
            "waiting": 0
        },
        {
            "name": "Product1",
            "sold": 12,
            "waiting": 0
        },
        {
            "name": "Product9",
            "sold": 4,
            "waiting": 0
        }
    ]
};

getCategoryStatistics0 = lambda : {
    "statistics": [
        "Category0",
        "Category1",
        "Category2",
        "Category3",
        "Category4",
        "Category5",
        "Category6"
    ]
};

getOrder3 = lambda: {
    "requests": [
        {
            "id"      : "Product4",
            "quantity": 22
        },
        {
            "id"      : "Product6",
            "quantity": 22
        }
    ]
};

getProductStatistics1 = lambda :{
    "statistics": [
        {
            "name": "Product0",
            "sold": 4,
            "waiting": 0
        },
        {
            "name": "Product1",
            "sold": 12,
            "waiting": 0
        },
        {
            "name": "Product9",
            "sold": 4,
            "waiting": 0
        },
        {
            "name": "Product4",
            "sold": 22,
            "waiting": 18
        },
        {
            "name": "Product6",
            "sold": 22,
            "waiting": 19
        }
    ]
};

getCategoryStatistics1 = lambda : {
    "statistics": [
        "Category5",
        "Category6",
        "Category0",
        "Category1",
        "Category2",
        "Category3",
        "Category4"
    ]
};

getOrder4 = lambda: {
    "requests": [
        {
            "id"      : "Product7",
            "quantity": 15
        },
        {
            "id"      : "Product8",
            "quantity": 15
        },
        {
            "id"      : "Product5",
            "quantity": 25
        }
    ]
};

getProductStatistics2 = lambda : {
    "statistics": [
        {
            "name": "Product0",
            "sold": 4,
            "waiting": 0
        },
        {
            "name": "Product1",
            "sold": 12,
            "waiting": 0
        },
        {
            "name": "Product9",
            "sold": 4,
            "waiting": 0
        },
        {
            "name": "Product4",
            "sold": 22,
            "waiting": 18
        },
        {
            "name": "Product6",
            "sold": 22,
            "waiting": 19
        },
        {
            "name": "Product7",
            "sold": 15,
            "waiting": 10
        },
        {
            "name": "Product8",
            "sold": 15,
            "waiting": 13
        },
        {
            "name": "Product5",
            "sold": 25,
            "waiting": 21
        }
    ]
};

getCategoryStatistics2 = lambda : {
    "statistics": [
        "Category4",
        "Category3",
        "Category5",
        "Category6",
        "Category0",
        "Category1",
        "Category2"
    ]
};

getData5 = lambda: "\n".join ( [
    "Category6,Product4,15,10.00",
    "Category3,Product5,19,10.01",
    "Category5,Product6,17,10.02",
    "Category4,Product8,10,10.03",
] );

getProductStatistics3 = lambda : {
    "statistics": [
        {
            "name": "Product0",
            "sold": 4,
            "waiting": 0
        },
        {
            "name": "Product1",
            "sold": 12,
            "waiting": 0
        },
        {
            "name": "Product9",
            "sold": 4,
            "waiting": 0
        },
        {
            "name": "Product4",
            "sold": 22,
            "waiting": 3
        },
        {
            "name": "Product6",
            "sold": 22,
            "waiting": 2
        },
        {
            "name": "Product7",
            "sold": 15,
            "waiting": 10
        },
        {
            "name": "Product8",
            "sold": 15,
            "waiting": 3
        },
        {
            "name": "Product5",
            "sold": 25,
            "waiting": 2
        }
    ]
};

getSearchResult10 = lambda : {
    "categories": [
        "Category0",
        "Category1",
        "Category2",
        "Category6",
        "Category3",
        "Category5",
        "Category4"
    ],
    "products": [
        {
            "categories": [
                "Category0"
            ],
            "id": 1,
            "name": "Product0",
            "price": 20.44,
            "quantity": 0
        },
        {
            "categories": [
                "Category0"
            ],
            "id": 2,
            "name": "Product1",
            "price": 30.44,
            "quantity": 0
        },
        {
            "categories": [
                "Category0"
            ],
            "id": 10,
            "name": "Product9",
            "price": 41.3,
            "quantity": 0
        },
        {
            "categories": [
                "Category0",
                "Category1",
                "Category2"
            ],
            "id": 11,
            "name": "Product10",
            "price": 17.98,
            "quantity": 5
        },
        {
            "categories": [
                "Category1",
                "Category2"
            ],
            "id": 3,
            "name": "Product2",
            "price": 29.89,
            "quantity": 5
        },
        {
            "categories": [
                "Category2"
            ],
            "id": 4,
            "name": "Product3",
            "price": 37.36,
            "quantity": 4
        },
        {
            "categories": [
                "Category6"
            ],
            "id": 5,
            "name": "Product4",
            "price": 10.0,
            "quantity": 0
        },
        {
            "categories": [
                "Category3"
            ],
            "id": 6,
            "name": "Product5",
            "price": 10.01,
            "quantity": 0
        },
        {
            "categories": [
                "Category5"
            ],
            "id": 7,
            "name": "Product6",
            "price": 10.02,
            "quantity": 0
        },
        {
            "categories": [
                "Category4"
            ],
            "id": 8,
            "name": "Product7",
            "price": 47.75,
            "quantity": 0
        },
        {
            "categories": [
                "Category4"
            ],
            "id": 9,
            "name": "Product8",
            "price": 10.03,
            "quantity": 0
        }
    ]
};
