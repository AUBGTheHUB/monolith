import { FormProvider, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { RadioComponent } from '@/internal_library/RadioComponent/RadioComponent';
import { Button } from '@/components/ui/button';
import { InputComponent } from '@/internal_library/InputComponent/InputComponent';

const RADIO_OPTIONS = [
    { label: 'Yes', value: true },
    { label: 'No', value: false },
];

const baseSchema = z.object({});

const adminSchema = baseSchema.extend({
    // Expect the string "true"
    is_admin: z.literal(true),
    team_name: z.string().min(3, { message: 'Team name must be at least 3 characters.' }),
});

const nonAdminSchema = baseSchema.extend({
    // Accept the string "false" OR undefined
    is_admin: z.literal(false),
    team_name: z.string().optional(),
});
// Combine them with a **plain union**.
export const registrationSchema = z.union([nonAdminSchema, adminSchema]);

export default function RegistrationForm() {
    const form = useForm<z.infer<typeof registrationSchema>>({
        resolver: zodResolver(registrationSchema),
        defaultValues: {
            is_admin: false,
            team_name: '',
        },
    });

    const onSubmit = (data: z.infer<typeof registrationSchema>) => {
        console.log('Form submitted:', data);
    };

    return (
        <FormProvider {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="bg-white">
                <RadioComponent
                    control={form.control}
                    name="is_admin"
                    options={RADIO_OPTIONS}
                    groupLabel="Are you an admin?"
                />

                <InputComponent
                    control={form.control}
                    name="team_name"
                    label="Team Name"
                    type="text"
                    placeholder="Enter your team name"
                />

                <Button type="submit" className="text-black border border-black">
                    Register
                </Button>
            </form>
        </FormProvider>
    );
}
