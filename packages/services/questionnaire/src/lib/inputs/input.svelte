<script lang="ts">
    import { Step } from "@skeletonlabs/skeleton";

    import type { Question} from '$lib/inputs/types';
    import { InputType } from "$lib/inputs/types";

    export let question: Question;
    export let appendToAnswers: Function;

    let answer = ""

    const handleInput = (e: Event) => {
        answer = (e.currentTarget as HTMLInputElement).value;
    }

    const isImage = (content: string) => content.includes("http")

    $: {
        appendToAnswers(question.title, answer)
    }

</script>

<Step stepTerm="Question">

    <div class="flex flex-col justify-center items-center">
        <h1 class="text-center text-lg">{question.title}</h1>
        {#each question.structure as section}
            {#each section as content}
                {#if isImage(content)}
                    <!-- svelte-ignore a11y-missing-attribute -->
                    <img src={content} width="500px"/>
                {:else}
                    <h2>{content}</h2>
                {/if}
            {/each}
        {/each}

        <!-- there's a bug here on dark mode, characters won't show up -->
        {#if question.type === InputType.TextArea}
            <textarea bind:value={answer}/>
        {:else}
            <input type={question.type} on:input={handleInput}/>
        {/if}
    </div>
</Step>
