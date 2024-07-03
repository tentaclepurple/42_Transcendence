# FT_Trascendence

## Create self-signed certificate

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ./nginx/certs/example.key -out ./nginx/certs/example.crt
```