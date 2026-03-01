import { z } from 'zod';
import { FILE_RULES } from '@/globalValidation/fileRules.ts';

// 1. Shared fields used in both Add and Edit modes
const baseSchema = z.object({
    name: z.string().min(2, 'Name must be at least 2 characters.').max(50, 'Name must be less than 50 characters.'),
    position: z.string().min(2, 'Position must be at least 2 characters.').optional().or(z.literal('')),
    departments: z.array(z.enum(['Development', 'Marketing', 'Logistics', 'PR', 'Design'])).default([]),
    social_links: z.object({
        linkedin: z.string().url('Invalid LinkedIn URL').optional().or(z.literal('')),
        github: z.string().url('Invalid GitHub URL').optional().or(z.literal('')),
        website: z.string().url('Invalid Website URL').optional().or(z.literal('')),
    }),
});

// 2. Helper for reusable file validation logic (size and type)
const imageValidation = z
    .any()
    .refine((files) => !files || files.length === 0 || files[0].size <= FILE_RULES.MAX_SIZE, `Max file size is 5MB.`)
    .refine(
        (files) => !files || files.length === 0 || FILE_RULES.ACCEPTED_TYPES.includes(files[0].type),
        '.jpg, .jpeg, .png, .webp files are accepted.',
    );

// 3. Creation Schema (POST) - Image is REQUIRED
export const createTeamMemberSchema = baseSchema.extend({
    avatar: imageValidation.refine((files) => files?.length > 0, 'Profile image is required'),
});

// 4. Update Schema (PATCH) - Image is OPTIONAL
export const updateTeamMemberSchema = baseSchema.extend({
    avatar: imageValidation.optional(),
});

// Export types for use in your components
export type TeamMemberFormData = z.infer<typeof createTeamMemberSchema> | z.infer<typeof updateTeamMemberSchema>;
