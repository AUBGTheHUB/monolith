## <strong> Development</strong>:

If you get a `white screen` and nothing is loading:
Check the browser's console - most probably there is a rendering issue with some component.

If you get an error `unused var`:  
Put `// eslint-disable-next-line no-unused-vars` above the line or `// eslint-disable-line no-unused-vars` at the end of the line.

---

### <strong> Routes </strong>:

`/admin` - login screen for management panel

On login, if the API validates the client, the client gets a token which is stored in `localStorage`

When trying to access restricted routes, the client sends the token and validates itself once again.

`Create, Update and Delete` requests should pass the token in a `BEARER_TOKEN` header.

---

## <strong>How to use the management panel</strong>

### Add new (at the top of each page):

Is a panel where you can add new documents (e.g. Add a new member).

### Actions:

Is a panel where you can either update or delete a document (e.g. Remove an old member).

<strong>Please, refer to the guidelines whenever you are adding or updating documents.</strong>

## Form Guidelines:

### Logos and Profile Pictures are retrieved from Google Drive:

1. Upload the images to a specific public folder. Images should be heavily compressed. (300x300px)
2. [How to embed Google Drive images](https://stackoverflow.com/questions/15557392/how-do-i-display-images-from-google-drive-on-a-website)
3. Paste the link in the form (e.g. `https://drive.google.com/uc?export=view&id=0B6wwyazyzml-OGQ3VUo0Z2thdmc`)

### Links:

-   LinkedIn: Copy paste the member's LinkedIn url link in the form field.
-   Other links: urls should always be added with their transfer protocols ( `https://` or `http://` ).

### Department:

-   `Marketing`, `Design`, `Public Relations`, `Development`, `Logistics`

### Start Date, End Date:

-   Should be UTC format

###### In order to be able to do filtering by department in the future
