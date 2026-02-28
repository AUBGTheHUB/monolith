export type User = {
    name: string;
    username: string;
    avatarUrl: string;
    siteRole: string;
};

export type HubAdmin = {
    id: string;
    name: string;
    member_type: string;
    position: string;
    avatar_url: string;
    departments: string[];
    social_links: {
        github?: string;
        website?: string;
        linkedin?: string;
    };
    created_at: string;
    updated_at: string;
    site_role: string;
    username: string;
};

export type AuthenticatedAdmin = {
    access_token: string;
    id_token: string;
};
