'use client';

import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { Button } from '@/components/ui/button';
import { Form } from '@/components/ui/form';
import { RadioButton } from './internal_library/radioComponent';

const FormSchema = z.object({
    notificationPreference: z.string().min(1, { message: 'GRESHKA' }),
});

export function App() {
    const form = useForm<z.infer<typeof FormSchema>>({
        resolver: zodResolver(FormSchema),
        defaultValues: {
            notificationPreference: '',
        },
    });

    const onSubmit = (data: z.infer<typeof FormSchema>) => {
        console.log(data);
    };

    const radioOptions = [
        { label: 'All new messages', value: 'all' },
        { label: 'Direct messages and mentions', value: 'mentions' },
        { label: 'Nothing', value: 'none' },
    ];

    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="w-2/3 space-y-6">
                <RadioButton
                    control={form.control}
                    name="notificationPreference"
                    options={radioOptions}
                    groupLabel="Notify me about..."
                    groupClassName="space-y-4"
                    itemClassName="flex items-center space-x-3 space-y-0"
                    labelClassName="font-normal"
                    inputClassName="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
                />
                <Button type="submit">Submit</Button>
            </form>
        </Form>
    );
}

export default App;
