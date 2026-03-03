import { HubMember } from '@/types/hub-member.ts';

export type User = {
    name: string;
    username: string;
    avatar_url: string;
    site_role: string;
};

export type HubAdmin = HubMember & {
    site_role: string;
    username: string;
};

export type AuthenticatedAdmin = {
    access_token: string;
    id_token: string;
};
