# MAILING SERVICE (Cloud Function)
Cloud function for easily sending emails using the main The Hub gmail account.

ENDPOINT: https://europe-west3-cloudservices-378314.cloudfunctions.net/mailer

### Calls should be AUTHENTICATED
* How to fetch bearer token: 
```shell
gcloud auth print-identity-token
```
* How to make an authenticated call:
    * Pass it in the Authorization header - `BEARER <token-here>`
<img src="https://i.ibb.co/RCwJWwG/image.png" alt="image" border="0">

* How to authenticate our services (such as the GO API) towards the cloud function:
    * [Create a service account](https://console.cloud.google.com/iam-admin/serviceaccounts?referrer=search&authuser=1&project=cloudservices-378314)
    * [Give Function Invoker permissions to service account](https://console.cloud.google.com/iam-admin/iam?referrer=search&authuser=1&project=cloudservices-378314)
    * .gitignore the json file 
    * Generate access token within service ([GO Example](https://console.cloud.google.com/iam-admin/iam?referrer=search&authuser=1&project=cloudservices-378314))


### Example Payload:
```json
{
    "html": "<h1>This is the body of the email</h1>",
    "subject": "Subject of the email", 
    "receiver": "probablysomeone@mail.com"
}
```