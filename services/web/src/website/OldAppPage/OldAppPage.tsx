import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion';
import { zodResolver } from '@hookform/resolvers/zod';
import { useState } from 'react';
import { FormProvider, useForm } from 'react-hook-form';
import { Fragment } from 'react/jsx-runtime';
import { z } from 'zod';
import MockDataComponent from '../mockRequest/mockComponent';
import { RadioComponent } from '@/internal_library/RadioComponent/RadioComponent';
import { Button } from '@/components/ui/button';

const FormSchema = z.object({
    notificationPreference: z.string().min(1, { message: 'GRESHKA' }),
});

const RADIO_OPTIONS = [
    { label: 'All new messages', value: 'all' },
    { label: 'Direct messages and mentions', value: 'mentions' },
    { label: 'Nothing', value: 'none' },
];

export const OldAppPage = () => {
    const form = useForm<z.infer<typeof FormSchema>>({
        resolver: zodResolver(FormSchema),
        defaultValues: {
            notificationPreference: '',
        },
    });

    const onSubmit = (data: z.infer<typeof FormSchema>) => {
        console.log(data);
    };

    const [count, setCount] = useState(2);

    return (
        <Fragment>
            <h1>Vite + React</h1>
            <div className="card">
                <button onClick={() => setCount((count) => count + 1)}>count is {count}</button>
                <p>
                    Edit <code>src/App.tsx</code> and save to test HMR
                </p>
            </div>
            <p className="read-the-docs">Click on the Vite and React logos to learn more</p>
            <Accordion type="single" collapsible>
                <AccordionItem value="item-1">
                    <AccordionTrigger>Is it accessible?</AccordionTrigger>
                    <AccordionContent>Yes. It adheres to the WAI-ARIA design pattern.</AccordionContent>
                </AccordionItem>
            </Accordion>
            <MockDataComponent />
            <FormProvider {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="w-2/3 space-y-6">
                    <RadioComponent
                        control={form.control}
                        name="notificationPreference"
                        options={RADIO_OPTIONS}
                        groupLabel="Notify me about..."
                    />
                    <Button type="submit">Submit</Button>
                </form>
            </FormProvider>
        </Fragment>
    );
};
