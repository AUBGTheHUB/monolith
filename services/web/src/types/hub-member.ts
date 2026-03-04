import { z } from 'zod';

export enum Departments {
    All = 'All',
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
