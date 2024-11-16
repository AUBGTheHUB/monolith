'use client';

import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { z } from 'zod';

import { Button } from '@/components/ui/button';
import { Form } from '@/components/ui/form';
import { DropdownComponent } from '@/lib/reusable-components/dropdown';

const FormSchema = z.object({
    fruit: z.string().min(1, { message: 'Please select a fruit' }),
});

export function TestForm() {
    const form = useForm({
        resolver: zodResolver(FormSchema),
        defaultValues: {
            fruit: '',
        },
        mode: 'onTouched',
    });

    const label = 'Fruits';
    const placeholder = 'Select a fruit';
    const className = 'fruits';
    const items = [
        { name: 'Apple', value: 'apple' },
        { name: 'Banana', value: 'banana' },
        { name: 'Blueberry', value: 'blueberry' },
    ];

    function onSubmit(data: z.infer<typeof FormSchema>) {
        console.log(data);
    }

    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="w-2/3 space-y-6">
                <DropdownComponent
                    label={label}
                    placeholder={placeholder}
                    className={className}
                    items={items}
                    control={form.control}
                    name="fruit" // Must match a key in `FormSchema`
                />
                <Button type="submit">Submit</Button>
            </form>
        </Form>
    );
}
