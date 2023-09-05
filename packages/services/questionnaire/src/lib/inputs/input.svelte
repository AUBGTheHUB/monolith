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

<Step>
    <svelte:fragment slot="header">{""}</svelte:fragment>
    <div class="flex flex-col justify-center items-center h-max w-96">
        <div class="flex flex-col justify-center items-center space-y-10">
            {#if question.title !== ""}
                <h1 class="text-2xl">{question.title}</h1>
            {/if}

            {@html question.body}
            {#if question.type === InputType.TextArea}
                <textarea bind:value={answer} class="hub-input block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Write your response here:"/>
            {:else}
                <input bind:value={answer} type="text" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"/>
            {/if}
        </div>
    </div>
</Step>

<style>
    :global(ul) {
        list-style-type: '•';
    }

    :global(a) {
        color: greenyellow;
    }

    .hub-input {
        width: 500px;
        height: 100px;
    }

    @media only screen and (max-device-width: 800px){
        .hub-input {
            width: 300px;
            height: 200px;
        }
    }
</style>
