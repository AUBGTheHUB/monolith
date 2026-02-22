import { z } from 'zod';
import { FILE_RULES } from '@/globalValidation/fileRules.ts';

const RULES = {
    TITLE: { MIN: 3, MAX: 100 },
    TAG: { MAX: 10, MIN_CHAR: 1, MAX_CHAR: 30 },
};

export const pastEventSchema = z.object({
    title: z
        .string()
        .min(1, { message: 'Event name is required' })
        .min(RULES.TITLE.MIN, { message: `Event name must be at least ${RULES.TITLE.MIN} characters` })
        .max(RULES.TITLE.MAX, { message: `Event name must be less than ${RULES.TITLE.MAX} characters` }),

    cover_picture: z
        .any()
        .refine((files) => files?.length > 0, 'Cover picture file is required')
        .refine((files) => files?.[0]?.size <= FILE_RULES.MAX_SIZE, `Max file size is 5MB.`)
        .refine(
            (files) => FILE_RULES.ACCEPTED_TYPES.includes(files?.[0]?.type),
            '.jpg, .jpeg, .png, .webp files are accepted.',
        ),

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

export type PastEventFormData = z.infer<typeof pastEventSchema>;
