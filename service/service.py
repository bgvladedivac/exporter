import yaml
import sys
import requests
from flask import Flask, app, Response
from prometheus_client import Gauge, CollectorRegistry, generate_latest

app = Flask(__name__)


def parse_configuration(filename="./configuration.yml"):
    """Parse the intput configuration file."""
    with open(filename, "r") as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)


def handle_metrics():
    """Handles the creation and feed on metrics."""
    registry = CollectorRegistry()
    configuration = parse_configuration()
    urls = configuration["urls"]
    metrics = configuration["metrics"]

    print(metrics)

    for metric in metrics:
        if metric["type"] == "gauge":
            g = Gauge(
                metric["name"],
                metric["docs"],
                ["url"],
                registry=registry,
            )

        for url in urls:
            response = requests.get(url)
            status_code = response.status_code
            response_seconds = response.elapsed.total_seconds()

            if "up" in metric["name"]:
                if status_code == 200:
                    g.labels(url).set(1)
                else:
                    g.labels(url).set(0)
            if "ms" in metric["name"]:
                g.labels(url).set(response_seconds)
    return registry


@app.route("/metrics")
def metric():
    return Response(generate_latest(handle_metrics()), mimetype="text/plain")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5004)
