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
        answer = e.target.value;
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
    <div class="flex flex-col justify-center items-center h-max w-49 md:self-center">
        <div class="flex flex-col justify-center items-center space-y-10 sm:h-full">
            {#if question.title !== ''}
                <h1 class="text-2xl text-center">{question.title}</h1>
            {/if}

            {@html question.body}

            {#if question.type === InputType.TextArea}
                <textarea
                    bind:value={answer}
                    class="custom-width block p-2.5 w-full sm:w-95 md:w-85 lg:w-96 xl:w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                    placeholder="Write your response here:" />
            {:else if question.type === InputType.Email}
                <input
                    type="email"
                    on:input={onEmailChange}
                    value={answer}
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

    :global(textarea) {
        width: 100%;
    }

    @media (max-width: 900px) {
        :global(pre) {
            width: 100%;
            align-self: center;
            display: flex;
            justify-content: center;
        }

        :global(code pre) {
            align-self: center;
            display: flex;
            overflow-x: auto;
            align-self: center;
            width: 95vw;
            justify-content: flex-start;
        }

        :global(span) {
            font-size: 10px !important;
        }
        :global(button span) {
            font-size: 15px !important;
        }
    }

    @media (max-width: 399px) {
        .custom-width {
            width: 100%;
        }
    }

    @media (max-width: 290px) {
        :global(header) {
            display: none !important;
        }
    }
</style>
