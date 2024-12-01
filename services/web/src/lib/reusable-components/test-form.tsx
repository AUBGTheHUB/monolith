import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { z } from 'zod';

import { Button } from '@/components/ui/button';
import { Form } from '@/components/ui/form';
import { DropdownComponent } from '@/internal_library/DropdownComponent/DropdownComponent';

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

    function onSubmit(data: z.infer<typeof FormSchema>) {
        console.log(data);
    }

    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="w-2/3 space-y-6">
                <DropdownComponent
                    name="fruit"
                    label="Fruits"
                    placeholder="Select a fruit"
                    dropdownLabelClassName="dropdown-label"
                    selectValueClassName="select-value"
                    selectItemClassName="select-item"
                    items={[
                        { name: 'Apple', value: 'apple' },
                        { name: 'Banana', value: 'banana' },
                        { name: 'Blueberry', value: 'blueberry' },
                    ]}
                    control={form.control}
                />
                <Button type="submit">Submit</Button>
            </form>
        </Form>
    );
}
