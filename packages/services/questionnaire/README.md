# create-svelte

Everything you need to build a Svelte project, powered by [`create-svelte`](https://github.com/sveltejs/kit/tree/master/packages/create-svelte).

## Adding questionnaires
```bash
curl --location 'localhost:5173' \
--header 'Content-Type: application/json' \
--data '{
    "department": "pr",
    "questions": [
        {
            "title": "Who Am IIIIIII??????",
            "type": "textarea",
            "structure": [
                [
                    "Tell us a bit about yourself. What do you like doing in your free time? How did you get into programming?"
                ]
            ]
        },
        {
            "title": "Have you ever seen code like this?",
            "type": "textarea",
            "structure": [
                [
                    "This is React:",
                    "https://code.visualstudio.com/assets/docs/nodejs/reactjs/intellisense.png",
                    "https://code.visualstudio.com/assets/docs/nodejs/reactjs/bracket-matching.png"
                ],
                [
                    "This is Angular:",
                    "https://code.visualstudio.com/assets/docs/nodejs/angular/breakpoint.png",
                    "https://code.visualstudio.com/assets/docs/nodejs/angular/suggestions.png"
                ]
            ]
        },
        {
            "title": "What does this code do?",
            "type": "textarea",
            "structure": [
                [
                    "This some OOP code which is used for filtering out new developers:",
                    "https://www.freecodecamp.org/news/content/images/2020/02/2-1.png"
                ]
            ]
        },
        {
            "title": "What'\''s your AUBG email?",
            "type": "text",
            "structure": []
        }
    ]
}

'
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
