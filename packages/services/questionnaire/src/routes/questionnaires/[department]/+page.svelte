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
    let isDisabled = false;

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
                isDisabled = true;

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

<div class="custom-width sm:w-4/5 md:w-3/4 lg:w-1/2 xl:w-1/1 mx-auto mb-6">
    <Stepper class="stepper" stepTerm="Question" on:step={handleFormatting} on:complete={submitAnswers}>
        <div class="custom-height">
            {#each questions as question}
                <Input {question} {appendToAnswers} {isDisabled} />
            {/each}
        </div>
    </Stepper>
</div>

<style>
    @media (max-width: 640px) {
        .custom-width {
            width: 90%;
        }
    }

    @media (max-width: 900px) {
        .custom-height {
            min-height: 80vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
    }
</style>
