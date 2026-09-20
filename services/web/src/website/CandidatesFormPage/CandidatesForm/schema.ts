import { z } from 'zod';

// const baseSchema = z.object({
//     name: z
//         .string()
//         .min(1, { message: 'Name is required.' })
//         .min(3, { message: 'Name must be at least 3 characters long.' })
//         .max(50, { message: 'Name cannot exceed 50 characters.' })
//         .regex(/^[a-zA-Z\u0400-\u04FF\s-]+$/, {
//             message: `Name can only contain letters, spaces and '-'.`,
//         }),
//
//     email: z
//         .string()
//         .min(1, { message: 'Email is required' })
//         .email({ message: 'Invalid email format.' }),
//
//     tshirt_size: z.string().min(1, { message: 'Please select an option.' }),
//
//     university: z.string().min(1, { message: 'University is required.' }),
//
//     location: z
//         .string()
//         .min(1, { message: 'Location is required.' })
//         .min(3, { message: 'Location must be at least 3 characters long.' })
//         .max(100, { message: 'Location cannot exceed 100 characters.' }),
//
//     age: z
//         .number({ required_error: 'Age is required.' })
//         .int({ message: 'Age must be a whole number.' })
//         .min(16, { message: 'You must be at least 16 years old.' })
//         .max(69, { message: 'Age cannot exceed 69.' }),
//
//     source_of_referral: z.string().min(1, { message: 'Please select an option.' }),
//     programming_language: z.string().min(1, { message: 'Please select an option.' }),
//     programming_level: z
//         .string({ required_error: 'Please select an option.' })
//         .nonempty({ message: 'Please select an option.' }),
//
//     has_participated_in_hackaubg: z.boolean({ message: 'Please select an option.' }),
//     has_internship_interest: z.boolean({ message: 'Please select an option.' }),
//     has_participated_in_hackathons: z.boolean({ message: 'Please select an option.' }),
//     has_previous_coding_experience: z.boolean({ message: 'Please select an option.' }),
//     share_info_with_sponsors: z.boolean({ message: 'Please select an option.' }).refine((value) => value === true, {
//         message: 'Cannot participate unless you agree.',
//     }),
// });

// const adminSchema = baseSchema.extend({
//     registration_type: z.enum(['admin', 'invite_link']),
//     team_name: z
//         .string()
//         .min(3, 'Team name must be at least 3 characters.')
//         .max(30, { message: 'Team name cannot exceed 30 characters.' }),
// });

// const nonAdminSchema = baseSchema.extend({
//     registration_type: z.literal('random'),
//     team_name: z.string().optional(),
// });

// const mainAdminSchema = baseSchema
//     .extend({
//         registration_type: z.string({ message: 'Please select an option.' }),
//         team_name: z.string().optional(),
//     })
//     .superRefine((data, ctx) => {
//         if (data.registration_type === 'admin') {
//             if (!data.team_name || data.team_name.trim().length < 3) {
//                 ctx.addIssue({
//                     code: z.ZodIssueCode.too_small,
//                     minimum: 3,
//                     inclusive: true,
//                     type: 'string',
//                     message: 'Team name must be at least 3 characters.',
//                     path: ['team_name'],
//                 });
//             }
//             if (!data.team_name || data.team_name.trim().length > 20) {
//                 ctx.addIssue({
//                     code: z.ZodIssueCode.too_big,
//                     maximum: 20,
//                     inclusive: true,
//                     type: 'string',
//                     message: 'Team name must not exceed 20 characters.',
//                     path: ['team_name'],
//                 });
//             }
//         }
//     });
//
// const adminNonAdminUnion = z.discriminatedUnion('registration_type', [adminSchema, nonAdminSchema]);
//
// export const registrationSchema = z.union([mainAdminSchema, adminNonAdminUnion]);

const questionSchema = z.object({
    prompt: z.string(),
    options: z
        .array(z.string())
        .nullish()
        .transform((value) => value ?? []),
    answer: z
        .string()
        .or(z.array(z.string()))
        .nullable()
        .transform((value) => value ?? []),
    question_type: z.enum(['GENERAL', 'DEVELOPMENT', 'DESIGN', 'PR', 'MARKETING', 'LOGISTICS']),
    answer_type: z.enum(['TEXT', 'SINGLE_CHOICE', 'MULTIPLE_CHOICE']),
});

export const formSchema = z.object({
    departments: z.array(z.string()),
    generalQuestions: z.array(questionSchema),
    developmentQuestions: z.array(questionSchema),
    designQuestions: z.array(questionSchema),
    marketingQuestions: z.array(questionSchema),
    prQuestions: z.array(questionSchema),
    logisticsQuestions: z.array(questionSchema),
});
