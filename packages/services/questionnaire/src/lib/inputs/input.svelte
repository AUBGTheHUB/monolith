<script lang="ts">
    import { Step } from "@skeletonlabs/skeleton";

    type Question = {
        title: string,
        structure: string[][]
    }

    export let question: Question;
    export let appendToAnswers: Function;
    let answer = ""

    $: {
        appendToAnswers(question.title, answer)
    }

    const isImage = (content: string) => content.includes("http")
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
        <input bind:value={answer}/>
    </div>
</Step>
