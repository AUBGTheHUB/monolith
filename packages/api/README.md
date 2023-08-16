# Old Golang API

> **Note:** When deploying, ensure to include the IP in the MongoDB configuration.

---

### Endpoint Structure:

**NB:** The `bearer_token` is not passed in an Authorization header but in a custom basic one - "BEARER-TOKEN".

#### Admins (used for authorization):

Requests:
- Post request on `/api/login` (login) - Accepts `username` and `password` in the request body, returns a bearer token upon success.
- Post request on `/api/validate` (BEARER-TOKEN validation) - Accepts a header with BEARER-TOKEN.

---

#### Members (used for managing club members):

Requests:
- Post request on `/api/member` (create member) - Accepts a bearer token in the header and member details in the form data.
- Get request on `/api/members` (get all members) - Empty request, returns all members.
- Get request on `/api/member/:key` (get single member) - Accepts a parameter `key` (memberid) in the URL.
- Put request on `/api/member/:key` (change info of member) - Accepts a parameter `key` (memberid) in the URL, event details in the form data, and a bearer token.
- Delete request on `/api/member/:key` (delete member) - Accepts a parameter `key` (memberid) in the URL and a bearer token in the header.

_Note: GET requests are not subject to authorization._

---

#### Jobs (used for managing displayed job opportunities):

Requests:
- Post request on `/api/job` (create job) - Accepts a bearer token in the header and job details in the form data.
- Get request on `/api/job/:key` (get job) - Accepts a `key` parameter and returns the job document.
- Get request on `/api/job` (get all jobs) - No parameters needed, returns all jobs.
- Put request on `/api/job/:key` (edit job) - Accepts a bearer token and job details in the form data.
- Delete request on `/api/job/:key` (delete job) - Accepts a bearer token.

---

#### Mentors:

Requests:
- Post request on `/api/mentors` (create mentor) - Accepts a bearer token in the header and mentor details in the form data.
- Get request on `/api/mentors/:key` (get mentor) - Accepts a `key` parameter and returns the mentor document.
- Get request on `/api/mentors` (get all mentors) - No parameters needed, returns all mentors.
- Put request on `/api/mentors/:key` (edit mentor) - Accepts a bearer token and mentor details in the form data.
- Delete request on `/api/mentors/:key` (delete mentor) - Accepts a bearer token.

---

#### Jury:

Requests:
- Post request on `/api/jury` (create jury) - Accepts a bearer token in the header and jury details in the form data.
- Get request on `/api/jury/:key` (get jury) - Accepts a `key` parameter and returns the jury document.
- Get request on `/api/jury` (get all jury) - No parameters needed, returns all jury.
- Put request on `/api/jury/:key` (edit jury) - Accepts a bearer token and jury details in the form data.
- Delete request on `/api/jury/:key` (delete jury) - Accepts a bearer token.

---

#### Sponsors:

Requests:
- Post request on `/api/sponsors` (create sponsor) - Accepts a bearer token in the header and sponsor details in the form data.
- Get request on `/api/sponsors/:key` (get sponsor) - Accepts a `key` parameter and returns the sponsor document.
- Get request on `/api/sponsors` (get all sponsors) - No parameters needed, returns all sponsors.
- Put request on `/api/sponsors/:key` (edit sponsor) - Accepts a bearer token and sponsor details in the form data.
- Delete request on `/api/sponsors/:key` (delete sponsor) - Accepts a bearer token.

---

#### Partners:

Requests:
- Post request on `/api/partners` (create partner) - Accepts a bearer token in the header and partner details in the form data.
- Get request on `/api/partners/:key` (get partner) - Accepts a `key` parameter and returns the partner document.
- Get request on `/api/partners` (get all partners) - No parameters needed, returns all partners.
- Put request on `/api/partners/:key` (edit partner) - Accepts a bearer token and partner details in the form data.
- Delete request on `/api/partners/:key` (delete partner) - Accepts a bearer token.

---
