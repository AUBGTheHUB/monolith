import { z } from 'zod';

const RULES = {
    NAME: { MIN: 2, MAX: 100 },
    COMPANY: { MIN: 2, MAX: 100 },
};

export const judgeSchema = z.object({
    name: z
        .string()
        .min(1, { message: 'Name is required' })
        .min(RULES.NAME.MIN, { message: `Name must be at least ${RULES.NAME.MIN} characters` })
        .max(RULES.NAME.MAX, { message: `Name must be less than ${RULES.NAME.MAX} characters` }),

    companyName: z
        .string()
        .min(1, { message: 'Company name is required' })
        .min(RULES.COMPANY.MIN, { message: `Company name must be at least ${RULES.COMPANY.MIN} characters` })
        .max(RULES.COMPANY.MAX, { message: `Company name must be less than ${RULES.COMPANY.MAX} characters` }),

    imageUrl: z
        .string()
        .min(1, { message: 'Image URL is required' })
        .url({ message: 'Please enter a valid URL (e.g., https://example.com/image.png)' }),
});


export type JudgeFormData = z.infer<typeof judgeSchema>;
