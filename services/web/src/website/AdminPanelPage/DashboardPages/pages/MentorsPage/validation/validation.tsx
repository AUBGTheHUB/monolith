import { z } from 'zod';

const RULES = {
    NAME: { MIN: 2, MAX: 100 },
    COMPANY: { MIN: 2, MAX: 100 },
};

export const mentorSchema = z.object({
    name: z
        .string()
        .min(1, { message: 'Name is required' })
        .min(RULES.NAME.MIN, { message: `Name must be at least ${RULES.NAME.MIN} characters` })
        .max(RULES.NAME.MAX, { message: `Name must be less than ${RULES.NAME.MAX} characters` }),

    company: z
        .string()
        .min(1, { message: 'Company name is required' })
        .min(RULES.COMPANY.MIN, { message: `Company name must be at least ${RULES.COMPANY.MIN} characters` })
        .max(RULES.COMPANY.MAX, { message: `Company name must be less than ${RULES.COMPANY.MAX} characters` }),

    avatar_url: z
        .string()
        .min(1, { message: 'Image URL is required' })
        .url({ message: 'Please enter a valid URL (e.g., https://example.com/image.png)' }),

    job_title: z.string().optional(),

    linkedin_url: z
        .string()
        .min(1, { message: 'Linkedin URL is required' })
        .url({ message: 'Please enter a valid URL (e.g., https://linkedin.com/in/username)' }),
});

export type MentorFormData = z.infer<typeof mentorSchema>;
