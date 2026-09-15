import { z } from 'zod';

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
