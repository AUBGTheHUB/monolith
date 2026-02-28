import { z } from 'zod';
import { DEPARTMENT_OPTIONS } from '../../../../../constants.ts';

export const registerSchema = z
    .object({
        username: z.string().min(3, 'Username must be at least 3 characters'),
        password: z.string().min(6, 'Password must be at least 6 characters'),
        repeat_password: z.string().min(6, 'Repeat password must be at least 6 characters'),
        name: z.string().nonempty('Name should not be empty'),
        position: z.string().nonempty('Position should not be empty'),
        avatar_url: z.string().url('Avatar url should be a valid url'),
        departments: z.array(z.enum(DEPARTMENT_OPTIONS)).min(1, 'Choose at least one department').default([]),
        github: z.string().url('Github should be a valid url').or(z.literal('')).optional(),
        linkedin: z.string().url('LinkedIn should be a valid url').or(z.literal('')).optional(),
        website: z.string().url('Website should be a valid url').or(z.literal('')).optional(),
    })
    .refine((data) => data.password === data.repeat_password, {
        message: 'Passwords do not match',
        path: ['repeat_password'],
    })
    .transform(({ github, linkedin, website, ...rest }) => {
        const social_links: Record<string, string> = {};

        if (github) social_links.github = github;
        if (linkedin) social_links.linkedin = linkedin;
        if (website) social_links.website = website;

        return {
            ...rest,
            social_links,
        };
    });

export type RegisterFormFields = z.input<typeof registerSchema>;
export type RegisterFormPayload = z.output<typeof registerSchema>;
