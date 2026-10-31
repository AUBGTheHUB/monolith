import { z } from 'zod';

const RULES = {
    NAME: { MIN: 2, MAX: 100 },
};

export const attendeeSchema = z.object({
    name: z
        .string()
        .min(1, { message: 'Name is required' })
        .min(RULES.NAME.MIN, { message: `Name must be at least ${RULES.NAME.MIN} characters` })
        .max(RULES.NAME.MAX, { message: `Name must be less than ${RULES.NAME.MAX} characters` }),

    email: z.string().min(1, { message: 'Email is required' }).email({ message: 'Please enter a valid email' }),

    ticket_type: z.enum(['guest', 'participant'], { errorMap: () => ({ message: 'Please select a ticket type' }) }),

    has_paid: z.boolean({
        required_error: 'Please select whether the ticket is paid',
        invalid_type_error: 'Please select whether the ticket is paid',
    }),
});

export type AttendeeFormData = z.infer<typeof attendeeSchema>;
