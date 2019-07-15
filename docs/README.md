# prometheus-url-checker

This little script periodically checks all configured urls with a HTTP HEAD request. The requests http code will be returned as prometheus compatible metric (gauge).

## Install

The packages uses the `flit` packager and requires `python 3.6`.

* `pip3 install flit`
* `flit install`

## Usage

The application is very simple to configure. Simply set the `URLS` environment variable and start the server with `prom-url-checker`. You can see the metrics opening `http://127.0.0.1:9999/metrics`. To integrate this into your prometheus environment, simply add a new prometheus endpoint.

A very simple cli allows the configuration of all necessary parameters.

* `prom-url-checker` starts the metrics server on `127.0.0.1:9999` using the `URLS` environmental variable
* `prom-url-checker --help` show's available cli options:

```bash
Options:
--host=STR            Host ip to serve on. (default: 127.0.0.1)
--port=STR            Port to use (default: 9999)
-s, --sleeptime=INT   Sleeptime during checks (default: 5)
--urls=STR            Comma seperated list of urls to check, e.g. --urls https://test.domain.de,http://domain.de.  If unset, the environment variable URLS will be used instead.
-d, --debug           Enable debugging mode

Other actions:
-h, --help            Show the help
```

## Metrics

```
# HELP request_in_progress Number of requests in progress
# TYPE request_in_progress gauge
request_in_progress{app="url_health_checker",host="f8cad31124a6",route="/"} 0

# HELP url_health Health status of a url.
# TYPE url_health gauge
url_health{app="url_health_checker",host="f8cad31124a6",url="https://google.com"} 301
url_health{app="url_health_checker",host="f8cad31124a6",url="https://github.com"} 200

# HELP url_health_request_processing_seconds Time spent processing request
# TYPE url_health_request_processing_seconds summary
url_health_request_processing_seconds{app="url_health_checker",host="f8cad31124a6",quantile="0.5"} 0.17756042900145985
url_health_request_processing_seconds{app="url_health_checker",host="f8cad31124a6",quantile="0.9"} 0.2960943900034181
url_health_request_processing_seconds{app="url_health_checker",host="f8cad31124a6",quantile="0.99"} 0.2960943900034181
url_health_request_processing_seconds_count{app="url_health_checker",host="f8cad31124a6"} 14
url_health_request_processing_seconds_sum{app="url_health_checker",host="f8cad31124a6"} 3.8046043350186665
```