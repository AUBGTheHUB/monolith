import { z } from 'zod';
import { FILE_RULES } from '@/globalValidation/fileRules.ts';

const RULES = {
    NAME: { MIN: 2, MAX: 100 },
    TIER: { MIN: 2, MAX: 50 },
};

// 1. Shared fields used in both Add and Edit modes
const baseSchema = z.object({
    name: z
        .string()
        .min(1, { message: 'Sponsor name is required' })
        .min(RULES.NAME.MIN, { message: `Name must be at least ${RULES.NAME.MIN} characters` })
        .max(RULES.NAME.MAX, { message: `Name must be less than ${RULES.NAME.MAX} characters` }),

    tier: z
        .string()
        .min(1, { message: 'Sponsorship tier is required' })
        .min(RULES.TIER.MIN, { message: `Tier must be at least ${RULES.TIER.MIN} characters` }),

    website_url: z.string().min(1, { message: 'Website URL is required' }).url({ message: 'Please enter a valid URL' }),
});

// 2. Helper for shared file validation logic (size and type)
const logoFileValidation = z
    .any()
    .refine((files) => !files || files.length === 0 || files?.[0]?.size <= FILE_RULES.MAX_SIZE, `Max file size is 5MB.`)
    .refine(
        (files) => !files || files.length === 0 || FILE_RULES.ACCEPTED_TYPES.includes(files?.[0]?.type),
        '.jpg, .jpeg, .png, .webp files are accepted.',
    );

// 3. Schema for POST (Creation) - Logo is REQUIRED
export const createSponsorSchema = baseSchema.extend({
    logo: logoFileValidation.refine((files) => files?.length > 0, 'Logo file is required'),
});

// 4. Schema for PATCH (Update) - Logo is OPTIONAL
export const updateSponsorSchema = baseSchema.extend({
    logo: logoFileValidation.optional(),
});

// Export a union type for the form components to use
export type SponsorFormData = z.infer<typeof createSponsorSchema> | z.infer<typeof updateSponsorSchema>;
