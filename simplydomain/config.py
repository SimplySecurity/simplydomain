import json


__json_config = {

    "meta_data": {
        "version": 0.1,
        "author": "Alexander Rymdeko-Harvey",
        "twitter": "Killswitch-GUI",
        "github_repo": "https://github.com/killswitch-GUI/SimplyDomain"
    },
    "subdomain_bruteforce": {
        "top_1000": [
            "third_party",
            "dnspop",
            "results",
            "bitquark_20160227_subdomains_popular_1000"
        ],
        "top_10000": [
            "third_party",
            "dnspop",
            "results",
            "bitquark_20160227_subdomains_popular_10000"
        ],
        "top_100000": [
            "third_party",
            "dnspop",
            "results",
            "bitquark_20160227_subdomains_popular_100000"
        ],
        "top_1000000": [
            "third_party",
            "dnspop",
            "results",
            "bitquark_20160227_subdomains_popular_1000000"
        ]
    },
    "yahoo_search": {
        "start_count": 0,
        "end_count": 1000,
        "quantity": 100,
        "sleep_time": 3,
        "sleep_jitter": 0.30
    },
    "bing_search": {
        "start_count": 1,
        "end_count": 100,
        "sleep_time": 3,
        "sleep_jitter": 0.30
    }

}
