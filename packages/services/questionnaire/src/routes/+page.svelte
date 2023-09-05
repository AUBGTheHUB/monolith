<script lang="ts">
    import { onMount } from "svelte";
    let location = ""

    onMount(() => {
        location = window.location.toString()
    })

    const handleChangeLocation = () => {
        // dark mode breaks if anchor tags are being used
        window.location.href = location + "demo"
    }
</script>

<h1 class="text-center">In order to be able to access a questionnaire, you need to append the name of the department to the url - <p on:click={handleChangeLocation}>{location + "demo"}</p></h1>
