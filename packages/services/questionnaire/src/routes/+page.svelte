<script lang="ts">
    /* TODO:
        1. add a database connection - https://github.com/stolinski/svelte-kit-mongodb-example
        2. add post endpoint in +server.js - https://learn.svelte.dev/tutorial/post-handlers
        3. add a submit button for making the POST request
    */
    import { LightSwitch } from '@skeletonlabs/skeleton';
    import { Stepper} from '@skeletonlabs/skeleton';

    import questionsData from "$lib/inputs/questions.json"
    import Input from "$lib/inputs/input.svelte";
    import type { Question } from '$lib/inputs/types';


    const answers: Record<string, string> = {}
    const questions: Question[] = questionsData as Question[]

    // function below is being passed down to components in order for them to be able
    // to append their answers to the object which is then to be used as the body for
    // the POST request --- TIP: do console.log(answers) in order to see what the function does
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
