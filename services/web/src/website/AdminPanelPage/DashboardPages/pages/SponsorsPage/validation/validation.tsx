import { z } from 'zod';
import { FILE_RULES } from '@/globalValidation/fileRules.ts';

const RULES = {
    NAME: { MIN: 2, MAX: 100 },
    TIER: { MIN: 2, MAX: 50 },
};

export const sponsorSchema = z.object({
    name: z
        .string()
        .min(1, { message: 'Sponsor name is required' })
        .min(RULES.NAME.MIN, { message: `Name must be at least ${RULES.NAME.MIN} characters` })
        .max(RULES.NAME.MAX, { message: `Name must be less than ${RULES.NAME.MAX} characters` }),

    tier: z
        .string()
        .min(1, { message: 'Sponsorship tier is required' })
        .min(RULES.TIER.MIN, { message: `Tier must be at least ${RULES.TIER.MIN} characters` }),

    logo: z
        .any()
        .refine((files) => files?.length > 0, 'Logo file is required')
        .refine((files) => files?.[0]?.size <= FILE_RULES.MAX_SIZE, `Max file size is 5MB.`)
        .refine(
            (files) => FILE_RULES.ACCEPTED_TYPES.includes(files?.[0]?.type),
            '.jpg, .jpeg, .png, .webp files are accepted.',
        ),

    website_url: z.string().min(1, { message: 'Website URL is required' }).url({ message: 'Please enter a valid URL' }),
});

export type SponsorFormData = z.infer<typeof sponsorSchema>;
