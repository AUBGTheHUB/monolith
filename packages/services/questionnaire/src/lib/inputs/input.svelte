<script lang="ts">
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

<div style="display: flex; flex-direction: column;justify-content: center; align-items: center;">
    <h1>{question.title}</h1>

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

    <input bind:value={answer}/>
</div>
