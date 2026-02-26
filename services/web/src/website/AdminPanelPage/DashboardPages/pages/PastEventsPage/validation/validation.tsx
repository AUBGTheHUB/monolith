import { z } from 'zod';
import { FILE_RULES } from '@/globalValidation/fileRules.ts';

const RULES = {
    TITLE: { MIN: 3, MAX: 100 },
    TAG: { MAX: 10, MIN_CHAR: 1, MAX_CHAR: 30 },
};

// 1. Shared fields used in both Add and Edit modes
const baseSchema = z.object({
    title: z
        .string()
        .min(1, { message: 'Event name is required' })
        .min(RULES.TITLE.MIN, { message: `Event name must be at least ${RULES.TITLE.MIN} characters` })
        .max(RULES.TITLE.MAX, { message: `Event name must be less than ${RULES.TITLE.MAX} characters` }),

    tags: z
        .array(
            z
                .string()
                .min(RULES.TAG.MIN_CHAR, { message: 'Tag is too short' })
                .max(RULES.TAG.MAX_CHAR, { message: 'Tag is too long' }),
        )
        .max(RULES.TAG.MAX, `Event must have fewer than ${RULES.TAG.MAX} tags`)
        .optional(),
});

// 2. Helper for shared file validation logic
const coverPictureValidation = z
    .any()
    .refine((files) => !files || files.length === 0 || files[0]?.size <= FILE_RULES.MAX_SIZE, `Max file size is 5MB.`)
    .refine(
        (files) => !files || files.length === 0 || FILE_RULES.ACCEPTED_TYPES.includes(files[0]?.type),
        '.jpg, .jpeg, .png, .webp files are accepted.',
    );

// 3. Schema for POST (Creation) - Cover Picture is REQUIRED
export const createPastEventSchema = baseSchema.extend({
    cover_picture: coverPictureValidation.refine((files) => files?.length > 0, 'Cover picture file is required'),
});

// 4. Schema for PATCH (Update) - Cover Picture is OPTIONAL
export const updatePastEventSchema = baseSchema.extend({
    cover_picture: coverPictureValidation.optional(),
});

// Export a union type for the form components to use
export type PastEventFormData = z.infer<typeof createPastEventSchema> | z.infer<typeof updatePastEventSchema>;
