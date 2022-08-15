# Backend for @TheHubAUBG's SPA

* Make sure you include IP in the mongodb configuration when deploying

<a href="https://github.com/asynchroza/Hub-Website-Backend/blob/main/go.mod"> Dependencies </a>
---
### Endpoint structure:

<p><strong>NB:</strong> bearer_token is not passed in an Authorization header but in a custom basic one - "BEARER_TOKEN" </p>
<p><strong>Admins (used for authorization): </p></strong>
<p>Requests: </p> 
<li> Post request on /api/login (login) - accepts username and password as body, and returns bearer token on success </li>
<li> Post request on /api/validate (BEARER_TOKEN validation) - accepts header with BEARER_TOKEN </li>
<hr/>
<p><strong>Members (used for managing club members):</p></strong>
<p>Requests:</p>
<li> Post request on /api/member (create member) - accepts bearer token as a header, member body as form data </li>
<li> Get request on /api/members (get all members) - empty request, returns all members </li>
<li> Get request on /api/member/:key (get single member) - accepts parameter key (memberid) (pass as ../member/1 not ../?key=1)</li>
<li> Put request on /api/member/:key (change info of member) - accepts parameter key (memberid), event body as form data and bearer token</li>
<li> Delete request on /api/member/:key (delete member) - accepts parameter key (memberid) and bearer token as a header</li>
<br>
<p><em><strong>NB:</strong> GET requests are not subject to authorization</em></p>
<hr/>
<p><strong>Events (used for managing displayed events): </p></strong>
<p><em><a href="http://www.timestamp-converter.com/">Use this website to convert dates to ISO format</a></em></p>
<li> Post request on /api/event (create event) - accepts bearer token as a header and event body as form data</li>
<li> Get request on /api/event/:key (get event) - accepts key parameter and returns indexed event (eventid) </li>
<li> Get request on /api/event (get all events) - no parameters needed, returns all events </li>
<li> Put request on /api/event/:key (edit event) - accepts bearer_token, event body as form data </li>

* Delete request on /api/event/:key (delete event) - accepts bearer token

<hr/>
<p><strong>Articles (used for managing displayed articles): </p></strong>

* Post request on /api/article (create article) - accepts bearer token as a header and article body as form data
* Get request on /api/job/:key (get article) - accepts key parameter and returns article document
* Get request on /api/article (get all articles) - no parameters needed, returns all articles
* Put request on /api/article (edit article) - accepts bearer token, article body as form data
* Delete request on /api/article/:key (delete article) - accepts bearer token

<hr/>
<p><strong>Jobs (used for managing displayed job opportunities): </p></strong>

* Post request on /api/job (create job) - accepts bearer token as a header and job body as form data
* Get request on /api/job/:key (get job) - accepts key parameter and returns job document
* Get request on /api/job (get all jobs) - no parameters needed, returns all jobs
* Put request on /api/job/:key (edit job) - accepts bearer token, job body as form data
* Delete request on /api/job/:key (delete job) - accepts bearer token

<hr/>

#### Mentors

* Post request on /api/mentors (create mentor) - accepts bearer token as a header and jury body as form data
* Get request on /api/mentors/:key (get mentor) - accepts key parameter and returns mentor document
* Get request on /api/mentors (get all mentors) - no parameters needed, returns all mentors
* Put request on /api/mentors/:key (edit mentor) - accepts bearer token, jury body as form data
* Delete request on /api/mentors/:key (delete mentor) - accepts bearer token

<hr/>


#### Jury

* Post request on /api/jury (create jury) - accepts bearer token as a header and jury body as form data
* Get request on /api/jury/:key (get jury) - accepts key parameter and returns jury document
* Get request on /api/jury (get all jury) - no parameters needed, returns all jury
* Put request on /api/jury/:key (edit jury) - accepts bearer token, jury body as form data
* Delete request on /api/jury/:key (delete jury) - accepts bearer token

<hr/>

#### Sponsors

* Post request on /api/sponsors (create sponsor) - accepts bearer token as a header and sponsor body as form data
* Get request on /api/sponsors/:key (get sponsor) - accepts key parameter and returns sponsor document
* Get request on /api/sponsors (get all sponsors) - no parameters needed, returns all sponsors
* Put request on /api/sponsors/:key (edit sponsor) - accepts bearer token, sponsor body as form data
* Delete request on /api/sponsors/:key (delete sponsor) - accepts bearer token


#### Partners

* Post request on /api/partners (create partner) - accepts bearer token as a header and sponsor body as form data
* Get request on /api/partners/:key (get partner) - accepts key parameter and returns partner document
* Get request on /api/partners (get all partners) - no parameters needed, returns all partners
* Put request on /api/partners/:key (edit partner) - accepts bearer token, sponsor body as form data
* Delete request on /api/partners/:key (delete partner) - accepts bearer token



> Tasks:  
> 2. Clean up readme - rewrite it only in markdown  
