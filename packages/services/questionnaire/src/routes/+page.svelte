<script lang="ts">
    /* TODO:
        * Add a submit button for making the POST request
        * Add a new input component for taking the user's name, email and bio on the same screen - type "about"
        * Make textareas and text inputs wider
        * Fix bug with text not showing on dark mode
        * (Optionally) add schema validation for POST request
    */
    import Input from "$lib/inputs/input.svelte";
    import { page } from '$app/stores';
    import { LightSwitch } from '@skeletonlabs/skeleton';
    import { Stepper} from '@skeletonlabs/skeleton';
    import { onMount } from "svelte";
    import { getHighlighter, type Highlighter } from "shiki";

    const questions = $page.data.questions;
    const answers: Record<string, string> = {}

    const appendToAnswers = (title: string, answer: string) => {answers[title] = answer}

    const formatCode = (highlighter: Highlighter, parser: DOMParser) => {
        const codeElements = document.querySelectorAll('code');
        codeElements.forEach(code => {
            // primitive language support for the club's most used languages
            const language = code.className?.includes("python") ? "python" : "js";
            const highlightedCode = highlighter.codeToHtml(code.textContent as string, {lang: language})
            code.innerHTML = highlightedCode;
        })
    }

    onMount(async ()=> {
        const parser = new DOMParser();
        formatCode(await getHighlighter({theme: "nord", langs: ["js", "python"]}), parser)
    })
</script>

<div class="flex flex-col justify-center items-center">
    <LightSwitch/>
    <Stepper>
        {#each questions as question}
            <Input {question} {appendToAnswers}/>
        {/each}
    </Stepper>
</div>
