<script lang="ts">
    /* TODO:
        1. add a database connection - https://github.com/stolinski/svelte-kit-mongodb-example
        2. add post endpoint in +server.js - https://learn.svelte.dev/tutorial/post-handlers
        3. add a submit button for making the POST request
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
        <!-- if you wonder how you need to handle the POST method here -->
        <!-- check the events section here - https://www.skeleton.dev/components/steppers -->
        {#each questions as question}
            <Input {question} {appendToAnswers}/>
        {/each}
    </Stepper>
</div>
