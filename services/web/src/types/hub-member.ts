export interface HubMember {
    id: string;
    name: string;
    position: string;
    departments: string[];
    avatar_url: string;
    social_links: {
        linkedin?: string | null;
        github?: string | null;
        website?: string | null;
    };
}
