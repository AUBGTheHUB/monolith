import { z } from 'zod';
import { DEPARTMENT_OPTIONS } from '@/constants.ts';
import { FILE_RULES } from '@/globalValidation/fileRules.ts';

export const registerSchema = z
    .object({
        username: z.string().min(3, 'Username must be at least 3 characters'),
        password: z.string().min(6, 'Password must be at least 6 characters'),
        repeat_password: z.string().min(6, 'Repeat password must be at least 6 characters'),
        name: z.string().nonempty('Name should not be empty'),
        position: z.string().min(2, 'Position must be at least 2 characters.').optional().or(z.literal('')),
        avatar: z
            .any()
            .refine(
                (files) => !files || files.length === 0 || files[0].size <= FILE_RULES.MAX_SIZE,
                `Max file size is 5MB.`,
            )
            .refine(
                (files) => !files || files.length === 0 || FILE_RULES.ACCEPTED_TYPES.includes(files[0].type),
                '.jpg, .jpeg, .png, .webp files are accepted.',
            )
            .refine((files) => files?.length > 0, 'Profile image is required'),
        departments: z.array(z.enum(DEPARTMENT_OPTIONS)).default([]),
        social_links: z.object({
            linkedin: z.string().url('Invalid LinkedIn URL').optional().or(z.literal('')),
            github: z.string().url('Invalid GitHub URL').optional().or(z.literal('')),
            website: z.string().url('Invalid Website URL').optional().or(z.literal('')),
        }),
    })
    .refine((data) => data.password === data.repeat_password, {
        message: 'Passwords do not match',
        path: ['repeat_password'],
    });

export type RegisterFormData = z.infer<typeof registerSchema>;
