# create-svelte

Everything you need to build a Svelte project, powered by [`create-svelte`](https://github.com/sveltejs/kit/tree/master/packages/create-svelte).

## Adding a questionnaire

You can add questionnaires by making POST requests to `/`.
### Example payload
* If you don't want to render a title or a body you may leave them as empty strings.
* `body` property is markdown parsable text.
* `type` defines the input type. Big/small input box or selectable options: `"textarea", "text"`.
```json
{
    "department": "demo",
    "questions": [
        {
            "title": "What is this javascript snippet doing?",
            "type": "textarea",
            "body": "```javascript\ndocument.getElementById('testBox').onkeypress = function(e) {\n\tvar evt = e ? e : window.event;\n\tif (evt.keyCode == 13) {\n\t\tdocument.getElementById('enterButton').click();\n\treturn false;\n\t}\n}\n```"
        },
        {
            "title": "Can you explain the difference between null and undefined in javascript?",
            "type": "textarea",
            "body": ""
        }
    ]
}
```

## Creating a project

If you're seeing this, you've probably already done this step. Congrats!

```bash
# create a new project in the current directory
npm create svelte@latest

# create a new project in my-app
npm create svelte@latest my-app
```

## Developing

Once you've created a project and installed dependencies with `npm install` (or `pnpm install` or `yarn`), start a development server:

```bash
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

## Building

To create a production version of your app:

```bash
npm run build
```

You can preview the production build with `npm run preview`.

> To deploy your app, you may need to install an [adapter](https://kit.svelte.dev/docs/adapters) for your target environment.
