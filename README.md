# Building Container
docker build . -t fdns

# Running
docker run -it -p 53:9999 fdns

# Running with another DNSServer
docker run -it -p 53:9999 -e "DNSSERVER=8.8.8.8"  fdns
