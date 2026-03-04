import { z } from 'zod';
import { FILE_RULES } from '@/globalValidation/fileRules.ts';

const RULES = {
    NAME: { MIN: 2, MAX: 100 },
    COMPANY: { MIN: 2, MAX: 100 },
};

// Shared fields between Add and Edit
const baseSchema = z.object({
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
    job_title: z.string().optional(),
    linkedin_url: z
        .string()
        .min(1, { message: 'Linkedin URL is required' })
        .url({ message: 'Please enter a valid URL' }),
});

// Helper for file validation logic
const fileValidation = z
    .any()
    .refine((files) => !files || files.length === 0 || files[0].size <= FILE_RULES.MAX_SIZE, `Max file size is 5MB.`)
    .refine(
        (files) => !files || files.length === 0 || FILE_RULES.ACCEPTED_TYPES.includes(files[0].type),
        '.jpg, .jpeg, .png, .webp files are accepted.',
    );

// 1. Schema for POST (Creation) - Avatar is REQUIRED
export const createJudgeSchema = baseSchema.extend({
    avatar: fileValidation.refine((files) => files?.length > 0, 'Avatar file is required'),
});

// 2. Schema for PATCH (Update) - Avatar is OPTIONAL
export const updateJudgeSchema = baseSchema.extend({
    avatar: fileValidation.optional(),
});

// Export a union type for the form components to use
export type JudgeFormData = z.infer<typeof createJudgeSchema> | z.infer<typeof updateJudgeSchema>;
