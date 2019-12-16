## Running

### Building Container
```
docker build . -t fdns
```

### Running
```
docker run -it -p 53:9999 fdns
```

### Running with another DNSServer
```
docker run -it -p 53:9999 -e "DNSSERVER=8.8.8.8"  fdns
```


## Questions


### Imagine this proxy being deployed in an infrastructure. What whould be the security concerns you would raise?

- We could enchance security by tunning the security settings. For instance, creating the security settings
from scratch relying on the Operation System bundle with the CA Certificates.

```
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations("/etc/ssl/certs/ca-bundle.crt")
```

- The lack of testability is a prominent issue. A better validation strategy as part of a Continuous Integration process that simulates for instance a fake UPStream DNS service responding with invalid certificates.


### How would you integrate that solution in a distributed, micro services-oriented and containerized architecture.

- It could be run as a deamonset, handling all the requests between containern whithin a Kubernetes Cluster, decreasing the risk of a man-in-the-middle over the internal DNS traffic.

- The microservices itself shouldn't have any control of it.

- Better observability to have insights about potential performance bottlenecks, error rates, and generic logs. It would need to be implemented as a non-blocking-process not to penalize overall performance, 



#### What other improvements do you think would be interesting to add to the project


- Better validation strategy and defensive programming. For example: if the query is a valid DNS query; if a real and whitelisted upstream server is being used and proper exception management.

- UDP implementation, (which I started but didn't finish due to lack of time to handle a technicality converting the UDP message bytes to TCP using the Python Socket Library.)

- Minimize the latency overhead due to the TLS, decreasing the number of new TCP connections created. With more time, I would investigate the recommendation for a local DNS request aggregator as mentioned here: https://tools.ietf.org/id/draft-ietf-dprive-dns-over-tls-05.html#rfc.section.5


