/** @type {import('@sveltejs/kit').HandleServerError} */
export function handleError({ error }: { error: any }) {
    console.log(error);
    return {
        message: 'Something went wrong!',
    };
}
