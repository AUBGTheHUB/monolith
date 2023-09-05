<script lang="ts">
    /* TODO:
        * Add a submit button for making the POST request
        * Add a new input component for taking the user's name, email and bio on the same screen - type "about"
        * (Optionally) add schema validation for POST request
    */
    import Input from "$lib/inputs/input.svelte";
    import { page } from '$app/stores';
    import { Stepper} from '@skeletonlabs/skeleton';
    import { getHighlighter, type Highlighter } from "shiki";
    import { onMount } from "svelte";

    const questions = $page.data.questions;
    const answers: Record<string, string> = {}

    const appendToAnswers = (title: string, answer: string) => {answers[title] = answer}

    let highlighter = null;

    const formatCode = (highlighter: Highlighter) => {
        const codeElements = document.querySelectorAll('code');
        codeElements.forEach(code => {
            // primitive language support for the club's most used languages
            const language = code.className?.includes("python") ? "python" : "js";
            const highlightedCode = highlighter.codeToHtml(code.textContent as string, {lang: language})
            code.innerHTML = highlightedCode;
        })
    }

    const handleFormatting = async () => {
        highlighter = await getHighlighter({theme: "nord", langs: ["js", "python"]})
        formatCode(highlighter)
    }

    onMount(async () => {
        handleFormatting()
    })
</script>

<div class="flex flex-col justify-center items-center">
    <Stepper stepTerm="Question" justify="justify-around" on:step={handleFormatting}>
        {#each questions as question}
            <Input {question} {appendToAnswers}/>
        {/each}
    </Stepper>
</div>
