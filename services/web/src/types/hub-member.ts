import { z } from 'zod';
import { zDateTime } from './utils';

export enum Departments {
    All = 'All',
    Board = 'Board',
    PR = 'PR',
    Design = 'Design',
    Development = 'Development',
    Marketing = 'Marketing',
    Logistics = 'Logistics',
}

export const zBaseHubMember = z.strictObject({
    id: z.string(),
    name: z.string(),
    position: z.string(),
    departments: z.array(z.nativeEnum(Departments)),
    avatar_url: z.string(),
    social_links: z.strictObject({
        linkedin: z.string().url().optional(),
        github: z.string().url().optional(),
        website: z.string().url().optional(),
    }),
});

export type BaseHubMember = z.infer<typeof zBaseHubMember>;

export const zHubMember = zBaseHubMember.extend({
    id: z.string(),
    username: z.string(),
    member_type: z.string(), // todo add enum once known
    position: z.string(), // todo add enum once known
    site_role: z.string(), // todo add enum once known
    created_at: zDateTime,
    updated_at: zDateTime,
})

export type HubMember = z.infer<typeof zHubMember>;
