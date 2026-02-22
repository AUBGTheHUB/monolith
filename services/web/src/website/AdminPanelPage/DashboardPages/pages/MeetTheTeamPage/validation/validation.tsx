import { z } from 'zod';

// Zod schema for the frontend form data. This is what the form will use for validation.
export const teamMemberFormSchema = z.object({
    name: z.string().min(2, 'Name must be at least 2 characters.').max(50, 'Name must be less than 50 characters.'),
    position: z.string().min(2, 'Position is required.'),
    departments: z.array(z.enum(['Development', 'Marketing', 'Logistics', 'PR', 'Design'])).default([]),
    avatar_url: z.string().url('Please enter a valid URL for the image.'),
    social_links: z.object({
        linkedin: z.string().url('Invalid LinkedIn URL').optional().or(z.literal('')),
        github: z.string().url('Invalid GitHub URL').optional().or(z.literal('')),
        website: z.string().url('Invalid Website URL').optional().or(z.literal('')),
    }),
});

export type TeamMemberFormData = z.infer<typeof teamMemberFormSchema>;
