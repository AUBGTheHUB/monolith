export type User = {
    name: string;
    username: string;
    avatar_url: string;
    site_role: string;
};

export type AuthenticatedAdmin = {
    access_token: string;
    id_token: string;
};
