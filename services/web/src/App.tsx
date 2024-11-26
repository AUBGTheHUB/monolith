import './App.css';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { Button } from '@/components/ui/button';
import { Form } from '@/components/ui/form';
import { RadioComponent } from './internal_library/RadioComponent';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@radix-ui/react-accordion';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import MockDataComponent from './website/mockComponent';
import reactLogo from './assets/react.svg';
import viteLogo from '/vite.svg';
import { useState } from 'react';

const FormSchema = z.object({
    notificationPreference: z.string().min(1, { message: 'GRESHKA' }),
});

const RADIO_OPTIONS = [
    { label: 'All new messages', value: 'all' },
    { label: 'Direct messages and mentions', value: 'mentions' },
    { label: 'Nothing', value: 'none' },
];

function App() {
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
    const queryClient = new QueryClient();
    return (
        <QueryClientProvider client={queryClient}>
            <div>
                <a href="https://vitejs.dev" target="_blank" rel="noreferrer">
                    <img src={viteLogo} className="logo" alt="Vite logo" />
                </a>
                <a href="https://react.dev" target="_blank" rel="noreferrer">
                    <img src={reactLogo} className="logo react" alt="React logo" />
                </a>
            </div>
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
            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="w-2/3 space-y-6">
                    <RadioComponent
                        control={form.control}
                        name="notificationPreference"
                        options={RADIO_OPTIONS}
                        groupLabel="Notify me about..."
                    />
                    <Button type="submit">Submit</Button>
                </form>
            </Form>
        </QueryClientProvider>
    );
}

export default App;
