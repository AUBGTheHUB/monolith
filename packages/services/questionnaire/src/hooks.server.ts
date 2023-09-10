/** @type {import('@sveltejs/kit').HandleServerError} */
export function handleError({ error }: { error: Error }) {
    console.log(error);
    return {
        message: 'Something went wrong! Are you missing a query parameter?',
    };
}
