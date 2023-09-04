<script lang="ts">
    /* TODO:
        * Add a submit button for making the POST request
        * Add a new input component for taking the user's name, email and bio on the same screen - type "about"
        * Make textareas and text inputs wider
        * Fix bug with text not showing on dark mode
        * (Optionally) add schema validation for POST request
    */
    import Input from "$lib/inputs/input.svelte";
    import { page } from '$app/stores';
    import { LightSwitch } from '@skeletonlabs/skeleton';
    import { Stepper} from '@skeletonlabs/skeleton';

    const questions = $page.data.questions;
    const answers: Record<string, string> = {}

    const appendToAnswers = (title: string, answer: string) => {answers[title] = answer}
</script>

<div class="flex flex-col justify-center items-center">
    <LightSwitch/>
    <Stepper>
        {#each questions as question}
            <Input {question} {appendToAnswers}/>
        {/each}
    </Stepper>
</div>
