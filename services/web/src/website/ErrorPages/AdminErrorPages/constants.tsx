export type ErrorData = {
    code: number;
    message: string;
    title: string;
};

export const ERROR_403: ErrorData = {
    code: 403,
    message: 'This Hubzie does not have access to the wanted page',
    title: 'Forbidden',
};

export const ERROR_404: ErrorData = {
    code: 404,
    message: 'Searched Address Not Found. It seems like Hubzie took a wrong turn!',
    title: 'Not Found',
};
