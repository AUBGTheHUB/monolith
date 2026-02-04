import { z } from 'zod';

export const teamMemberSchema = z.object({
    name: z
        .string()
        .min(1, { message: 'Name is required' })
        .min(2, { message: 'Name must be at least 2 characters' })
        .max(50, { message: 'Name must be less than 50 characters' }),

    departments: z.array(z.string()).min(1, { message: 'At least one department is required' }),

    image: z.string().optional(),
});

export type TeamMemberFormData = z.infer<typeof teamMemberSchema>;
