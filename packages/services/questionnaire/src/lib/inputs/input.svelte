<script lang="ts">
    import { Step } from "@skeletonlabs/skeleton";
    import { compile } from 'mdsvex';


    import type { Question } from '$lib/inputs/types';
    import { InputType } from "$lib/inputs/types";

    export let question: Question;
    export let appendToAnswers: Function;

    let answer = ""

    const handleInput = (e: Event) => {
        answer = (e.currentTarget as HTMLInputElement).value;
    }

    $: {
        appendToAnswers(question.title, answer)
    }

</script>

<Step stepTerm="Question">

    <div class="flex flex-col justify-center items-center">
        <h1 class="text-center text-lg">{question.title}</h1>
            <div class="prose">
                {@html question.body}
            </div>

        <!-- there's a bug here on dark mode, characters won't show up -->
        {#if question.type === InputType.TextArea}
            <textarea bind:value={answer}/>
        {:else}
            <input type={question.type} on:input={handleInput}/>
        {/if}
    </div>
</Step>

<style>
    .prose :is(h2, h3, h4, h5, h6) {
	/* margin-top: var(--size-8); */
	/* margin-bottom: var(--size-3); */
    }

    .prose p:not(:is(h2, h3, h4, h5, h6) + p) {
        /* margin-top: var(--size-7); */
    }

    .prose :is(ul, ol) {
        /* list-style-type: '🔥'; */
        /* padding-left: var(--size-5); */
    }

    .prose :is(ul, ol) li {
        /* margin-block: var(--size-2); */
        /* padding-inline-start: var(--size-2); */
    }

    .prose pre {
        max-inline-size: 100%;
        padding: 1rem;
        border-radius: 8px;
        tab-size: 2;
    }
</style>
