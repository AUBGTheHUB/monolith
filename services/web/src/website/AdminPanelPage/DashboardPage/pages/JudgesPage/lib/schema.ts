import { z } from 'zod';
import { JUDGE_VALIDATION_RULES, JUDGE_VALIDATION_ERRORS } from './judges.validation';

export const judgeSchema = z.object({
    name: z
        .string()
        .min(1, { message: JUDGE_VALIDATION_ERRORS.NAME_REQUIRED })
        .min(JUDGE_VALIDATION_RULES.NAME.MIN_LENGTH, { message: JUDGE_VALIDATION_ERRORS.NAME_TOO_SHORT })
        .max(JUDGE_VALIDATION_RULES.NAME.MAX_LENGTH, { message: JUDGE_VALIDATION_ERRORS.NAME_TOO_LONG }),
    companyName: z
        .string()
        .min(1, { message: JUDGE_VALIDATION_ERRORS.COMPANY_REQUIRED })
        .min(JUDGE_VALIDATION_RULES.COMPANY.MIN_LENGTH, { message: JUDGE_VALIDATION_ERRORS.COMPANY_TOO_SHORT })
        .max(JUDGE_VALIDATION_RULES.COMPANY.MAX_LENGTH, { message: JUDGE_VALIDATION_ERRORS.COMPANY_TOO_LONG }),
    imageUrl: z.string().min(1, { message: JUDGE_VALIDATION_ERRORS.IMAGE_REQUIRED }),
});

export type JudgeSchema = z.infer<typeof judgeSchema>;
