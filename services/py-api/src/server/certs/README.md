### In this directory are stored the self-signed certs for localhost. This is in order to have a local env as close as possible to a production one.

### SSL certs for DEV environment
* `localhost.cert`
* `localhost.key`

### These certs were generated with the following command:
```bash
openssl req -x509 -newkey rsa:4096 -sha256 -days 3650 \
  -nodes -keyout localhost.key -out localhost.crt -subj "/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1,IP:0.0.0.0"
```
