import { z } from 'zod';
import { FILE_RULES } from '@/globalValidation/fileRules.ts';

// Zod schema for the frontend form data. This is what the form will use for validation.
export const teamMemberFormSchema = z.object({
    name: z.string().min(2, 'Name must be at least 2 characters.').max(50, 'Name must be less than 50 characters.'),
    position: z.string().min(2, 'Position is required.'),
    departments: z.array(z.enum(['Development', 'Marketing', 'Logistics', 'PR', 'Design'])).default([]),
    avatar: z
        .any()
        .refine((files) => files?.length > 0, 'Avatar file is required')
        .refine((files) => files?.[0]?.size <= FILE_RULES.MAX_SIZE, `Max file size is 5MB.`)
        .refine(
            (files) => FILE_RULES.ACCEPTED_TYPES.includes(files?.[0]?.type),
            '.jpg, .jpeg, .png, .webp files are accepted.',
        ),
    social_links: z.object({
        linkedin: z.string().url('Invalid LinkedIn URL').optional().or(z.literal('')),
        github: z.string().url('Invalid GitHub URL').optional().or(z.literal('')),
        website: z.string().url('Invalid Website URL').optional().or(z.literal('')),
    }),
});

export type TeamMemberFormData = z.infer<typeof teamMemberFormSchema>;
