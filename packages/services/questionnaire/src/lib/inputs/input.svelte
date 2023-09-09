<script lang="ts">
    import { Step } from '@skeletonlabs/skeleton';

    import type { Question } from '$lib/inputs/types';
    import { InputType } from '$lib/inputs/types';

    export let question: Question;
    export let appendToAnswers: Function;
    export let isDisabled: boolean;

    let answer = '';

    if (question.type === InputType.Email) {
        isDisabled = true;
    }

    const onEmailChange = (e: any) => {
        const regex = /^[A-Za-z0-9._%+-]+@aubg\.edu$/;
        if (regex.test(e.target.value)) {
            isDisabled = false;
        } else {
            isDisabled = true;
        }
    };

    $: {
        appendToAnswers(question.title, answer);
    }
</script>

<Step locked={isDisabled}>
    <svelte:fragment slot="header">{''}</svelte:fragment>
    <div class="flex flex-col justify-center items-center h-max w-96">
        <div class="flex flex-col justify-center items-center space-y-10">
            {#if question.title !== ''}
                <h1 class="text-2xl">{question.title}</h1>
            {/if}

            <p class="question-description">
                {@html question.body}
            </p>

            {#if question.type === InputType.TextArea}
                <textarea
                    bind:value={answer}
                    class="hub-input block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                    placeholder="Write your response here:" />
            {:else if question.type === InputType.Email}
                <input
                    type="email"
                    on:input={onEmailChange}
                    placeholder="Write your AUBG email:"
                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" />
            {:else}
                <input
                    bind:value={answer}
                    type="text"
                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" />
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

    .question-description {
        width: 100%;
        text-align: justify;
    }

    .hub-input {
        width: 500px;
        height: 100px;
        margin-bottom: 50px;
    }
    @media only screen and (max-width: 800px) {
        .hub-input {
            width: 475px;
        }
    }
    @media only screen and (max-width: 700px) {
        .hub-input {
            width: 300px;
            height: 200px;
        }

        .question-description {
            font-size: 13px;
            width: 85%;
            margin-bottom: 50px;
        }
    }
</style>
