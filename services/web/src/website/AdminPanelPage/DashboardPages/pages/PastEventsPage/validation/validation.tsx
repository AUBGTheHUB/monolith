import { z } from 'zod';

const RULES = {
    TITLE: { MIN: 3, MAX: 100 },
    TAG: { MIN: 1, MAX: 10, MIN_CHAR: 1, MAX_CHAR: 30 },
};

export const pastEventSchema = z.object({
    title: z
        .string()
        .min(1, { message: 'Event name is required' })
        .min(RULES.TITLE.MIN, { message: `Event name must be at least ${RULES.TITLE.MIN} characters` })
        .max(RULES.TITLE.MAX, { message: `Event name must be less than ${RULES.TITLE.MAX} characters` }),

    cover_picture: z
        .string()
        .min(1, { message: 'Image URL is required' })
        .url({ message: 'Please enter a valid URL (e.g., https://example.com/image.png)' }),

    tags: z
        .array(
            z
                .string()
                .min(RULES.TAG.MIN_CHAR, { message: 'Tag is too short' })
                .max(RULES.TAG.MAX_CHAR, { message: 'Tag is too long' }),
        )
        .min(RULES.TAG.MIN, `Event must have at least ${RULES.TAG.MIN} tags`)
        .max(RULES.TAG.MAX, `Event must have fewer than ${RULES.TAG.MAX} tags`)
        .optional(),
});

export type PastEventFormData = z.infer<typeof pastEventSchema>;
