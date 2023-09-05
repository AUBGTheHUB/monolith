<script lang="ts">
    import { Step } from "@skeletonlabs/skeleton";

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
            <div class="prose list-disc">
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
    /* TODO: Add additional stylings */
    :global(ul) {
        list-style-type: '•';
    }
</style>
