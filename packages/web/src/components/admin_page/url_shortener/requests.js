export const updateErrorMessage = (err, setErrorMessage) => {
    if (err.code === 'ERR_NETWORK') {
        setErrorMessage('API is not responding!');
    } else if (err?.response?.data?.detail?.[0]?.ctx?.error) {
        setErrorMessage('Not a viable URL - ' + err.response.data.detail[0].ctx.error + '!');
    } else {
        const message = err?.response?.data?.message ? err.response.data.message : 'Something went wrong!';
        setErrorMessage(message);
    }
};
