import { z } from 'zod';

const zDateTime = z.string().refine((val) => {
    const date = val.split(' ')[0];
    const time = val.split(' ')[1];

    const zDate = z.string().date()
    const zTime= z.string().time()

    return zDate.safeParse(date) && zTime.safeParse(time)
});

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
