import { z } from 'zod';

const RULES = {
    PROMPT: { MIN: 2, MAX: 100 },
    COMPANY: { MIN: 2, MAX: 100 },
};

// Shared fields between Add and Edit
export const baseSchema = z.object({
    prompt: z
        .string()
        .min(2, { message: 'Prompt is required' })
        .min(RULES.PROMPT.MIN, { message: `Prompt must be at least ${RULES.PROMPT.MIN} characters` })
        .max(RULES.PROMPT.MAX, { message: `Prompt must be less than ${RULES.PROMPT.MAX} characters` }),
    question_type: z.array(z.enum(['GENERAL', 'DEVELOPMENT', 'DESIGN', 'PR', 'MARKETING', 'LOGISTICS'])).default([]),
    answer_type: z.array(z.enum(['TEXT', 'SINGLE_CHOICE', 'MULTIPLE_CHOICE'])).default([]),
    // fix this one
    options: z.string().optional(),
});

// Export a union type for the form components to use
export type CandidateFormQuestionFormData = z.infer<typeof baseSchema>;
