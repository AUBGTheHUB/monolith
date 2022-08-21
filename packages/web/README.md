### Development:
If you get a `white screen` and nothing is loading:
Check the browser's console - most probably there is a rendering issue with some component

If you get an error `unused var`:  
Put `// eslint-disable-next-line no-unused-vars` above the line or `// eslint-disable-line no-unused-vars` at the end of the line.


### Routes:

`/admin` - login screen for management panel

On login, if the API validates the client, the client gets a token which is stored in `localStorage`

When trying to access restricted routes, the client sends the token and validates itself once again.

`Create, Update and Delete` should receive the token in a `BEARER_TOKEN` header.

## How to use the management panel

`url links` should always be added with their `https://` or `http://`.

### Members

#### Actions:

Accesses a page where you can either update a member with new information or delete it.  
Fields which are left empty won't be updated.

#### Drive Profile Picture:

1. Upload the images to a specific public folder. Images should be heavily compressed.
2. [How to Google Drive images](https://stackoverflow.com/questions/15557392/how-do-i-display-images-from-google-drive-on-a-website)
3. Paste the link in the form (e.g. `https://drive.google.com/uc?export=view&id=0B6wwyazyzml-OGQ3VUo0Z2thdmc`)

#### Linked Link:

Copy paste the member's LinkedIn url link in the form field.

#### Department:

Choose one: `Marketing`, `Design`, `Public Relations`, `Development`, `Logistics`

###### In order to be able to do filtering by department in the future
