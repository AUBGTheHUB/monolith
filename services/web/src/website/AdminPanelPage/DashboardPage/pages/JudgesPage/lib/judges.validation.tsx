import { z } from 'zod';

export const judgeSchema = z.object({
    name: z
        .string()
        .min(1, { message: 'Name is required' })
        .min(2, { message: 'Name must be at least 2 characters' })
        .max(100, { message: 'Name must be less than 100 characters' }),
    companyName: z
        .string()
        .min(1, { message: 'Company name is required' })
        .min(2, { message: 'Company name must be at least 2 characters' })
        .max(100, { message: 'Company name must be less than 100 characters' }),
    imageUrl: z.string().min(1, { message: 'Image URL is required' }),
});

export type JudgeFormData = z.infer<typeof judgeSchema>;
