```shell
# generate rsa private key of size 2048 with name 'jwt-private.pem'
openssl genrsa -out jwt-private.pem 2048
```

```shell
# extract the public key from the pair which can be used in a certificate
# command creates public key based on private key
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```
