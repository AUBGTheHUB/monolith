<script>
    import '../app.postcss';
    import { Toast, initializeStores } from '@skeletonlabs/skeleton';

    initializeStores();
</script>

<Toast />
<slot />
