<!-- Why is this not inserted into the properly colored body? -->
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
<div>
    <h1 class="text-center">In order to be able to access a questionnaire, you need to append the name of the department to the url - <p on:click={handleChangeLocation}>{location + "demo"}</p></h1>
    <img src="https://i.guim.co.uk/img/static/sys-images/Film/Pix/pictures/2013/8/28/1377708539760/Scarface---Al-Pacino--008.jpg?width=465&dpr=1&s=none" alt="tonimontana"/>
</div>
