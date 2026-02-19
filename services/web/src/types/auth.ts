export type HubAdmin = {
    id: string;
    name: string;
    member_type: string;
    position: string;
    avatar_url: string;
    department: string;
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

export type Authenticated = {
    access_token: string;
};
