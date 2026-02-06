import { z } from 'zod';

const RULES = {
    TITLE: { MIN: 3, MAX: 100 },
    TAG: { MIN: 1, MAX: 30 },
    LINK: { MAX: 200 },
    IMAGE_SIZE_MB: 5, // max 5 MB
};

export const pastEventSchema = z.object({
    title: z
        .string()
        .min(1, { message: 'Event name is required' })
        .min(RULES.TITLE.MIN, { message: `Event name must be at least ${RULES.TITLE.MIN} characters` })
        .max(RULES.TITLE.MAX, { message: `Event name must be less than ${RULES.TITLE.MAX} characters` }),

    image: z
        .string()
        .min(1, { message: 'Image URL is required' })
        .url({ message: 'Please enter a valid URL (e.g., https://example.com/image.png)' }),

    tags: z
        .array(
            z
                .string()
                .min(RULES.TAG.MIN, { message: 'Tag is too short' })
                .max(RULES.TAG.MAX, { message: 'Tag is too long' }),
        )
        .optional(),

    link: z
        .string()
        .url({ message: 'Please enter a valid URL (e.g., https://example.com/event)' })
        .max(RULES.LINK.MAX, { message: `Link must be less than ${RULES.LINK.MAX} characters` })
        .optional()
        .or(z.literal('')), // allow empty string
});

export type PastEventFormData = z.infer<typeof pastEventSchema>;
