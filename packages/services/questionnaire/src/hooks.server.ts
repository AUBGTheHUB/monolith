/** @type {import('@sveltejs/kit').HandleServerError} */
export function handleError({ error }: { error: any }) {
    console.error(error);

    return {
        message: 'Something went wrong! Are you missing a query parameter?',
        error,
    };
}
