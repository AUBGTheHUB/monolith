import { z } from 'zod';

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

    logoUrl: z
        .string()
        .min(1, { message: 'Logo URL is required' })
        .url({ message: 'Please enter a valid URL for the logo' }),

    websiteUrl: z.string().min(1, { message: 'Website URL is required' }).url({ message: 'Please enter a valid URL' }),

    careersUrl: z.string().optional().or(z.literal('')), // Allow empty string or valid URL
});

export type SponsorFormData = z.infer<typeof sponsorSchema>;
