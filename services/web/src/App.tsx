import './App.css';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { Button } from '@/components/ui/button';
import { Form } from '@/components/ui/form';
import { RadioComponent } from './internal_library/RadioComponent/RadioComponent';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@radix-ui/react-accordion';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import MockDataComponent from './website/mockComponent';
import reactLogo from './assets/react.svg';
import viteLogo from '/vite.svg';
import { useState } from 'react';
import { InputComponent } from './internal_library/InputComponent/InputComponent';

const FormSchema = z.object({
    notificationPreference: z.string().min(1, { message: 'GRESHKA' }),
    username: z
        .string()
        .min(1, { message: 'Required' })
        .min(3, { message: 'Username must be at least 3 characters long.' })
        .max(15, { message: 'Username cannot be more than 15 characters long.' })
        .regex(/^[a-zA-Z0-9_-]+$/, {
            message: 'Username can only contain letters, numbers, underscores, and dashes.',
        }),
    password: z
        .string()
        .min(1, { message: 'Required' })
        .min(8, { message: 'Password must be at least 8 characters long.' })
        .regex(/[A-Z]/, { message: 'Password must contain at least one uppercase letter.' })
        .regex(/[a-z]/, { message: 'Password must contain at least one lowercase letter.' })
        .regex(/[0-9]/, { message: 'Password must contain at least one number.' })
        .regex(/[@$!%*?&]/, { message: 'Password must contain at least one special character.' }),
    email: z
        .string()
        .min(1, { message: 'Required' })
        .email({ message: 'Invalid email format.' })
        .regex(/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/, {
            message: 'Please enter a valid email address.',
        }),
    firstName: z
        .string()
        .min(1, { message: 'Required' })
        .min(3, { message: 'First name must be at least 3 characters long.' })
        .max(20, { message: 'First name cannot be more than 20 characters long.' })
        .regex(/^[a-zA-Z]+$/, {
            message: 'Username can only contain letters.',
        }),
    lastName: z
        .string()
        .min(1, { message: 'Required' })
        .min(3, { message: 'Last name must be at least 3 characters long.' })
        .max(20, { message: 'Last name cannot be more than 20 characters long.' })
        .regex(/^[a-zA-Z]+$/, {
            message: 'Last name can only contain letters.',
        }),
    age: z
        .number()
        .int()
        .min(16, { message: 'Age must be at least 16.' })
        .max(69, { message: 'Age cannot be more than 69.' }),
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
            username: '',
            password: '',
            email: '',
            firstName: '',
            lastName: '',
            age: undefined,
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
                    <InputComponent
                        control={form.control}
                        name="email"
                        label="Email"
                        type="email"
                        placeholder="Enter your email"
                    />
                    <InputComponent
                        control={form.control}
                        name="username"
                        label="Username"
                        type="text"
                        placeholder="Enter your username"
                    />

                    <InputComponent
                        control={form.control}
                        name="password"
                        label="Password"
                        type="password"
                        placeholder="Enter your password"
                    />

                    <InputComponent
                        control={form.control}
                        name="firstName"
                        label="First Name"
                        type="text"
                        placeholder="Enter your first name"
                    />
                    <InputComponent
                        control={form.control}
                        name="lastName"
                        label="Last Name"
                        type="text"
                        placeholder="Enter your last name"
                    />

                    <InputComponent
                        control={form.control}
                        name="age"
                        label="Age"
                        type="number"
                        placeholder="Enter your age"
                    />
                    <Button type="submit">Submit</Button>
                </form>
            </Form>
        </QueryClientProvider>
    );
}

export default App;
