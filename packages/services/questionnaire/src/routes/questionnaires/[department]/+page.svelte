<script lang="ts">
    /* TODO:
     * Add a submit button for making the POST request
     * Add a new input component for taking the user's name, email and bio on the same screen - type "about"
     * (Optionally) add schema validation for POST request
     */
    import Input from '$lib/inputs/input.svelte';
    import { page } from '$app/stores';
    import { Stepper, type ToastSettings } from '@skeletonlabs/skeleton';
    import { getToastStore } from '@skeletonlabs/skeleton';
    import { getHighlighter, setCDN, type Highlighter } from 'shiki';
    import { onMount, tick } from 'svelte';

    const questions = $page.data.questions;
    const answers: Record<string, string> = {};
    const toastStore = getToastStore();

    setCDN('/questionnaires/shiki');

    const appendToAnswers = (title: string, answer: string) => {
        answers[title] = answer;
    };

    let highlighter: Highlighter | null = null;

    const formatCode = (highlighter: Highlighter) => {
        const codeElements = document.querySelectorAll('code');
        codeElements.forEach(code => {
            // primitive language support for the club's most used languages
            const language = code.className?.includes('python') ? 'python' : 'js';
            const highlightedCode = highlighter.codeToHtml(code.textContent as string, { lang: language });
            code.innerHTML = highlightedCode;
        });
    };

    const handleFormatting = async () => {
        await tick();
        formatCode(highlighter as Highlighter);
    };

    onMount(async () => {
        highlighter = await getHighlighter({ theme: 'nord', langs: ['js', 'python'] });
        handleFormatting();
    });

    const submitAnswers = async () => {
        const badToast: ToastSettings = {
            message: 'Something went wrong! Please, contact The Hub!',
            autohide: false,
            background: 'variant-filled-warning',
        };

        try {
            const body = JSON.stringify({ department: $page.data.department, answers });
            const response = await fetch(`/questionnaires/answers`, {
                body,
                method: 'POST',
            });

            if (response.ok) {
                const goodToast: ToastSettings = {
                    message:
                        'Answers were submitted! Thank you for participating! We hope we see you at the interviews!',
                    autohide: false,
                    background: 'variant-filled-primary',
                };
                toastStore.trigger(goodToast);

                setTimeout(() => {
                    location.href = 'https://thehub-aubg.com';
                }, 3000);
            } else {
                toastStore.trigger(badToast);
            }
        } catch (e) {
            console.error(e);
            toastStore.trigger(badToast);
        }
    };
</script>

<div class="flex flex-col justify-center items-center">
    <Stepper stepTerm="Question" justify="justify-around" on:step={handleFormatting} on:complete={submitAnswers}>
        {#each questions as question}
            <Input {question} {appendToAnswers} />
        {/each}
    </Stepper>
</div>
