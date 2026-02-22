export interface HubMember {
    id: string;
    name: string;
    member_type: 'member' | 'admin';
    position: string;
    departments: string[];
    avatar_url: string;
    social_links: {
        linkedin?: string | null;
        github?: string | null;
        website?: string | null;
    };
}
