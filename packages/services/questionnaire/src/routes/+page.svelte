<script lang="ts">
    /* TODO:
        1. add a database connection - https://github.com/stolinski/svelte-kit-mongodb-example
        2. add post endpoint in +server.js - https://learn.svelte.dev/tutorial/post-handlers
        3. add a submit button for making the POST request
    */
    import questions from "$lib/inputs/questions.json"
    import Input from "$lib/inputs/input.svelte";

    const answers: Record<string, string> = {}
    const appendToAnswers = (title: string, answer: string) => {answers[title] = answer}
</script>

<div style="display: flex; flex-direction: column; justify-content: center; align-items: center">
    {#each questions as question}
        <Input {question} {appendToAnswers}/>
    {/each}
</div>
