<script lang="ts">
    import { Step } from "@skeletonlabs/skeleton";

    import type { Question } from '$lib/inputs/types';
    import { InputType } from "$lib/inputs/types";
    import { afterUpdate, onMount } from "svelte";
    import { getHighlighter, type Highlighter } from "shiki";

    export let question: Question;
    export let appendToAnswers: Function;

    let answer = ""
    let highlighter: Highlighter | null = null;

    const handleInput = (e: Event) => {
        answer = (e.currentTarget as HTMLInputElement).value;
    }

    $: {
        appendToAnswers(question.title, answer)
    }


</script>

<Step>
    <svelte:fragment slot="header">{question.title}</svelte:fragment>
    <div class="flex flex-col justify-center items-center w-screen h-max">
        <div class="flex flex-col justify-center items-center space-y-10">
            {@html question.body}
            {#if question.type === InputType.TextArea}
                <textarea bind:value={answer} style="color: black;"/>
            {:else}
                <input type={question.type} on:input={handleInput} style="color: black;"/>
            {/if}
        </div>
    </div>
</Step>

<style>
    /* TODO: Add additional stylings */
    :global(ul) {
        list-style-type: '•';
    }

</style>
