import { z } from 'zod';

const imageSchema = z.union([z.instanceof(File), z.string().min(1)]).refine((val) => {
    if (val instanceof File) {
        return val.size <= 5 * 1024 * 1024;
    }
    return true;
}, 'Image must be smaller than 5MB');

export const pastEventSchema = z.object({
    title: z.string().min(3),
    image: imageSchema,
    tags: z.array(z.string()),
    link: z.string().url().optional().or(z.literal('')),
});

export type PastEventFormValues = z.infer<typeof pastEventSchema>;
