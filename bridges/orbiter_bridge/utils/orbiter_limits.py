MIN_VALUE_ASSETS = 0.1

transfer_limit = {
    'eth': {
        'arb': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0012
            },
            'usdc': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,

            },
            'usdt': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000
            },
            'dai': {
                'min': MIN_VALUE_ASSETS,
                'max': 3000
            },
        },
        'op': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0012,
            },
            'usdc': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000
            },
            'usdt': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000
            },
            'dai': {
                'min': MIN_VALUE_ASSETS,
                'max': 3000
            },
        },
        'matic': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0005
            },
            'usdc': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000
            },
            'usdt': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000
            },
            'dai': {
                'min': MIN_VALUE_ASSETS,
                'max': 3000
            },
        },
        'bsc': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0005
            },
        },
        'nova': {
            'eth': {
                'min': 0.005,
                'max': 5,
                'withholding_fee': 0.0005
            },
            'usdc': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000
            },
        },
        'lite': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0013
            },
            'usdc': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,

            },
            'usdt': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000
            },
            'dai': {
                'min': MIN_VALUE_ASSETS,
                'max': 3000
            },
        },
        'era': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0022
            }
        },
    },
    'arb': {
        'matic': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0006
            },
            'usdc': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 1.5
            },
            'usdt': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 1.5
            },
            'dai': {
                'min': MIN_VALUE_ASSETS,
                'max': 3000,
                'withholding_fee': 1.5
            },
        },
        'op': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0007
            },
            'usdc': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 2
            },
            'usdt': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 2
            },
            'dai': {
                'min': MIN_VALUE_ASSETS,
                'max': 3000,
                'withholding_fee': 2
            },
        },
        'eth': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0062
            },
            'usdc': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 12.8
            },
            'usdt': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 12.8
            },
            'dai': {
                'min': MIN_VALUE_ASSETS,
                'max': 3000,
                'withholding_fee': 12.8
            },
        },
        'bsc': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0003
            },
        },
        'nova': {
            'eth': {
                'min': 0.005,
                'max': 5,
                'withholding_fee': 0.0005
            },
            'usdc': {
                'min': MIN_VALUE_ASSETS,
                'max': 5000,
                'withholding_fee': 1.5
            },

        },
        'lite': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0013
            },
            'usdc': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 2
            },
            'usdt': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 2
            },
            'dai': {
                'min': MIN_VALUE_ASSETS,
                'max': 3000,
                'withholding_fee': 2
            },
        },
        'era': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0016
            }
        },
    },
    'op': {
        'matic': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0005
            },
            'usdc': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 1.5
            },
            'usdt': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 1.5
            },
            'dai': {
                'min': MIN_VALUE_ASSETS,
                'max': 3000,
                'withholding_fee': 1.5
            },
        },
        'arb': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0011
            },
            'usdc': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 1.8
            },
            'usdt': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 1.8
            },
            'dai': {
                'min': MIN_VALUE_ASSETS,
                'max': 3000,
                'withholding_fee': 1.8
            },
        },
        'eth': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0062
            },
            'usdc': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 12.8
            },
            'usdt': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 12.8
            },
            'dai': {
                'min': MIN_VALUE_ASSETS,
                'max': 3000,
                'withholding_fee': 12.8
            },
        },
        'bsc': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0003
            },
        },
        'nova': {
            'eth': {
                'min': 0.005,
                'max': 5,
                'withholding_fee': 0.0005
            },
            'usdc': {
                'min': MIN_VALUE_ASSETS,
                'max': 5000,
                'withholding_fee': 1
            },

        },
        'lite': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0013
            },
            'usdc': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 1.5
            },
            'usdt': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 1.5
            },
            'dai': {
                'min': MIN_VALUE_ASSETS,
                'max': 3000,
                'withholding_fee': 1.5
            },
        },
        'era': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0016
            }
        },
    },
    'matic': {
        'op': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0008
            },
            'usdc': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 2
            },
            'usdt': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 2
            },
            'dai': {
                'min': MIN_VALUE_ASSETS,
                'max': 3000,
                'withholding_fee': 2
            },
        },
        'arb': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0011
            },
            'usdc': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 2.5
            },
            'usdt': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 2.5
            },
            'dai': {
                'min': MIN_VALUE_ASSETS,
                'max': 3000,
                'withholding_fee': 2.5
            },
        },
        'eth': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0062
            },
            'usdc': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 12.8
            },
            'usdt': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 12.8
            },
            'dai': {
                'min': MIN_VALUE_ASSETS,
                'max': 3000,
                'withholding_fee': 12.8
            },
        },
        'bsc': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0003
            },
        },
        'nova': {
            'eth': {
                'min': 0.005,
                'max': 5,
                'withholding_fee': 0.0005
            },
            'usdc': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 2
            },

        },
        'lite': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0013
            },
            'usdc': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 2

            },
            'usdt': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 2
            },
            'dai': {
                'min': MIN_VALUE_ASSETS,
                'max': 3000,
                'withholding_fee': 2
            },
        },
        'era': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0016
            }
        },
    },
    'bsc': {
        'op': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0008
            },
        },
        'arb': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0008
            }
        },
        'eth': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0062
            }
        },
        'matic': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0003
            },
        },
        'nova': {
            'eth': {
                'min': 0.005,
                'max': 5,
                'withholding_fee': 0.0005
            },
        },
        'lite': {
            'eth': {
                'min': 0.005,
                'max': 5,
                'withholding_fee': 0.0013
            },
        },
        'era': {
            'eth': {
                'min': 0.005,
                'max': 5,
                'withholding_fee': 0.0016
            },
        },
    },
    'nova': {
        'op': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0005
            },
            'usdc': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 1
            },
            'usdt': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 1
            },
            'dai': {
                'min': MIN_VALUE_ASSETS,
                'max': 3000,
                'withholding_fee': 1
            },
        },
        'arb': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0006
            },
            'usdc': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 1
            },
            'usdt': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 1
            },
            'dai': {
                'min': MIN_VALUE_ASSETS,
                'max': 3000,
                'withholding_fee': 1
            },
        },
        'polygon': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0005
            },
            'usdc': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 1
            },
            'usdt': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 1
            },
            'dai': {
                'min': MIN_VALUE_ASSETS,
                'max': 3000,
                'withholding_fee': 1
            },
        },
        'eth': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0062
            },
            'usdc': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 12.8
            },

        },
        'bsc': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0005
            },
        },
        'lite': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0005
            },
            'usdc': {
                'min': MIN_VALUE_ASSETS,
                'max': 10,
                'withholding_fee': 1
            },
        },
        'era': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0005
            },
        }
    },
    'lite': {
        'arbitrum': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0011
            },
            'usdc': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 3
            },
            'usdt': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 3
            },
            'dai': {
                'min': MIN_VALUE_ASSETS,
                'max': 3000,
                'withholding_fee': 3
            },
        },
        'op': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0008,
            },
            'usdc': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 1.8,
            },
            'usdt': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 1.8,
            },
            'dai': {
                'min': MIN_VALUE_ASSETS,
                'max': 3000,
                'withholding_fee': 1.8,
            },
        },
        'matic': {
            'eth': {
                'min': 0.007,
                'max': 10,
                'withholding_fee': 0.0005
            },
            'usdc': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 1.5
            },
            'usdt': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 1.5
            },
            'dai': {
                'min': MIN_VALUE_ASSETS,
                'max': 3000,
                'withholding_fee': 1.5
            },
        },
        'bsc': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0005
            },
        },
        'nova': {
            'eth': {
                'min': 0.005,
                'max': 5,
                'withholding_fee': 0.0005
            },
            'usdc': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 1
            },
        },
        'eth': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0062
            },
            'usdc': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 12.8

            },
            'usdt': {
                'min': MIN_VALUE_ASSETS,
                'max': 10000,
                'withholding_fee': 12.8
            },
            'dai': {
                'min': MIN_VALUE_ASSETS,
                'max': 3000,
                'withholding_fee': 12.8
            },
        },
        'era': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0018
            },
        }
    },
    'era': {
        'arb': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0013
            },
        },
        'op': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0017,
            },
        },
        'matic': {
            'eth': {
                'min': 0.007,
                'max': 10,
                'withholding_fee': 0.0009
            },
        },
        'bsc': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0013
            },
        },
        'nova': {
            'eth': {
                'min': 0.005,
                'max': 5,
                'withholding_fee': 0.0008
            },
        },
        'eth': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0062
            }
        },
        'lite': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0012
            }
        }
    }
}
