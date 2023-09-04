<script>
    import {page} from "$app/stores"
</script>

<body class="dark min-h-screen min-w-full flex flex-col justify-center items-center text-white">
    <h1>{$page.status}</h1>
    <p>{$page.error?.message}</p>
</body>
