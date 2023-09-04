/** @type {import('@sveltejs/kit').HandleServerError} */
export function handleError({ error }: { error: any }) {
    return {
        message: 'Query parameter is either missing or incorrect!',
    };
}
