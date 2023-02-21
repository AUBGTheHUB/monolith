# MAILING SERVICE (Cloud Function)
Cloud function for easily sending emails using the main The Hub gmail account.

ENDPOINT: https://europe-west3-cloudservices-378314.cloudfunctions.net/mailer

## How to authenticate towards the function:
* Pass token (to be found in NOSYNCDEV team discussions) in Authorization header
<img src="https://i.ibb.co/c68pKPR/image.png" alt="image" border="0">

## Example Payload:
```json
{
    "html": "<h1>This is the body of the email</h1>",
    "subject": "Subject of the email", 
    "receiver": "probablysomeone@mail.com"
}
```

## How to test locally:
* Run/Debug function 
```python
make func-debug  # calls to be made towards http://127.0.0.1:8080
```

## Deploy function:
* Download and install the [GCP CLI](https://cloud.google.com/sdk/docs/install)
* Login and authenticate using the `CloudServices` project
* Deploy by running:
```python
make func-deploy
```

## Full Example (using POSTMAN):

### Sender:
<img src="https://i.ibb.co/cxt81Dq/image.png" alt="image" border="0">

### Receiver:
<img src="https://i.ibb.co/5h01Ybj/image.png" alt="image" border="0">
