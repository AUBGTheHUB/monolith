<script lang="ts">
    import questions from "$lib/inputs/questions.json"
    import Input from "$lib/inputs/input.svelte";

    const answers: Record<string, string> = {}
    const appendToAnswers = (title: string, answer: string) => {answers[title] = answer}
</script>

<div style="display: flex; flex-direction: column; justify-content: center; align-items: center">
    {#each questions as question}
        <Input {question} {appendToAnswers}/>
    {/each}
</div>
