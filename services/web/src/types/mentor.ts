import { z } from 'zod';
import { zDateTime } from './utils';

export const zMentor = z.strictObject({
    id: z.string(),
    name: z.string(),
    company: z.string(),
    job_title: z.string(),
    avatar_url: z.string(),
    linkedin_url: z.string().optional(),
    created_at: zDateTime,
    updated_at: zDateTime,
});

export type Mentor = z.infer<typeof zMentor>;
