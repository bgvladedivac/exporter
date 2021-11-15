
# Regarding the core python code
Once you hit the service there's a small delay. The delay comes from actually hitting the urls and creating/feeding the metrics. An improvement idea is to have a dedicated thread that takes care for creating and feeding the metrics. On a /metrics endpoint request from the user, the Flask would just 'ask' for the current status of those metrics from the thread. The metrics are handled in a dedicated prometheus registry.

# Regarding the Dockerfile
Decided to pull the 'curl' utility in the Dockerfile. Main reason is being able to 'validate' that everything is working as expected. In case you have started the container after building the image, you could check if the /metrics is acting as expected. In the below example 'crazy_dhawan' is the name of my container.

```
sudo docker exec -it crazy_dhawan curl localhost:5004/metrics
# HELP sample_external_url_up tracks http status code 200, 1 for true, 0 for false
# TYPE sample_external_url_up gauge
sample_external_url_up{url="https://httpstat.us/503"} 0.0
sample_external_url_up{url="https://httpstat.us/200"} 1.0
# HELP sample_external_url_response_ms tracks response http time
# TYPE sample_external_url_response_ms gauge
sample_external_url_response_ms{url="https://httpstat.us/503"} 0.347617
sample_external_url_response_ms{url="https://httpstat.us/200"} 0.329654
```

# Next steps to run the app in K8s.
The app already has a Docker image. The next natural step is to procude a pod template. Then we could also create a service and set proper labels to redirect the traffic to the pod. As a final step - we abstract easier rollouts in a deployment
No need for authentication (SA).

# Helm chart
There's a mandatory docker registry that you must provide in values.yaml. The chart
remains as simple as possibble.

# Verify app in K8s.
```
~ kubectl exec -it metrics-exposer-deploy-7458b5fc69-4ml9t -- curl localhost:5004/metrics
# HELP sample_external_url_up tracks http status code 200, 1 for true, 0 for false
# TYPE sample_external_url_up gauge
sample_external_url_up{url="https://httpstat.us/503"} 0.0
sample_external_url_up{url="https://httpstat.us/200"} 1.0
# HELP sample_external_url_response_ms tracks response http time
# TYPE sample_external_url_response_ms gauge
sample_external_url_response_ms{url="https://httpstat.us/503"} 0.314787
sample_external_url_response_ms{url="https://httpstat.us/200"} 0.363723
```

