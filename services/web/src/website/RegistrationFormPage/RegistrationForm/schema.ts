import { z } from 'zod';

const MAX_TEXT_LENGTH = 2000;

export const registrationSchema = z.object({
    first_name: z
        .string()
        .min(1, { message: 'First name is required.' })
        .min(2, { message: 'First name must be at least 2 characters long.' })
        .max(50, { message: 'First name must be at most 50 characters long.' }),

    last_name: z
        .string()
        .min(1, { message: 'Last name is required.' })
        .min(2, { message: 'Last name must be at least 2 characters long.' })
        .max(50, { message: 'Last name must be at most 50 characters long.' }),

    email: z
        .string()
        .min(1, { message: 'Email is required.' })
        .email({ message: 'Invalid email format.' }),

    country: z
        .string()
        .min(1, { message: 'Country is required.' }),

    address: z
        .string()
        .min(1, { message: 'Address is required.' })
        .max(200, { message: 'Address must be at most 200 characters long.' }),

    // Participation
    has_team: z
        .boolean({ required_error: 'Please select if you have a team.' }),

    role: z
        .string({ required_error: 'Please select a role.' })
        .min(1, { message: 'Please select a role.' }),

    has_participated_in_hackathons: z
        .boolean({ required_error: 'Please select an option.' }),

    idea: z
        .string()
        .min(1, { message: 'Please briefly describe your idea.' })
        .max(MAX_TEXT_LENGTH, { message: `Idea must be at most ${MAX_TEXT_LENGTH} characters long.` }),

    challenge: z
        .string()
        .min(1, { message: 'Please describe the challenge.' })
        .max(MAX_TEXT_LENGTH, { message: `Challenge must be at most ${MAX_TEXT_LENGTH} characters long.` }),

    motivation: z
        .string()
        .min(1, { message: 'Please tell us why you want to participate.' })
        .max(MAX_TEXT_LENGTH, { message: `Motivation must be at most ${MAX_TEXT_LENGTH} characters long.` }),

    best_describes: z
        .string({ required_error: 'Please select the trait that best describes you.' })
        .min(1, { message: 'Please select an option.' }),
});
