import { render, waitFor } from '@testing-library/react';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm, FormProvider, SubmitHandler } from 'react-hook-form';
import { z } from 'zod';
import { InputComponent } from './InputComponent';
import { Button } from '@/components/ui/button';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';

// Validation messages
const REQUIRED_MESSAGE = 'Required';
const USERNAME_MIN_LENGTH_MESSAGE = 'Username must be at least 3 characters long.';
const USERNAME_MAX_LENGTH_MESSAGE = 'Username cannot be more than 15 characters long.';
const USERNAME_REGEX_MESSAGE = 'Username can only contain letters, numbers, underscores, and dashes.';
const PASSWORD_MIN_LENGTH_MESSAGE = 'Password must be at least 8 characters long.';
const PASSWORD_UPPERCASE_MESSAGE = 'Password must contain at least one uppercase letter.';
const PASSWORD_LOWERCASE_MESSAGE = 'Password must contain at least one lowercase letter.';
const PASSWORD_NUMBER_MESSAGE = 'Password must contain at least one number.';
const PASSWORD_SPECIAL_CHAR_MESSAGE = 'Password must contain at least one special character.';
const EMAIL_INVALID_FORMAT_MESSAGE = 'Invalid email format.';
const AGE_MIN_MESSAGE = 'Age must be at least 16.';
const AGE_MAX_MESSAGE = 'Age cannot be more than 69.';

// Schema definition
const formSchema = z.object({
    username: z
        .string()
        .min(1, { message: REQUIRED_MESSAGE })
        .min(3, { message: USERNAME_MIN_LENGTH_MESSAGE })
        .max(15, { message: USERNAME_MAX_LENGTH_MESSAGE })
        .regex(/^[a-zA-Z0-9_-]+$/, { message: USERNAME_REGEX_MESSAGE }),
    password: z
        .string()
        .min(1, { message: REQUIRED_MESSAGE })
        .min(8, { message: PASSWORD_MIN_LENGTH_MESSAGE })
        .regex(/[A-Z]/, { message: PASSWORD_UPPERCASE_MESSAGE })
        .regex(/[a-z]/, { message: PASSWORD_LOWERCASE_MESSAGE })
        .regex(/[0-9]/, { message: PASSWORD_NUMBER_MESSAGE })
        .regex(/[@$!%*?&]/, { message: PASSWORD_SPECIAL_CHAR_MESSAGE }),
    email: z
        .string()
        .min(1, { message: REQUIRED_MESSAGE })
        .regex(/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/, { message: EMAIL_INVALID_FORMAT_MESSAGE }),
    age: z.number().min(16, { message: AGE_MIN_MESSAGE }).max(69, { message: AGE_MAX_MESSAGE }),
});

// Mock ResizeObserver
class ResizeObserver {
    observe() {}
    unobserve() {}
    disconnect() {}
}
global.ResizeObserver = ResizeObserver;

// Helper component
type FormInputProps = {
    onFormSubmit: SubmitHandler<z.infer<typeof formSchema>>;
};

const RenderInputComponent = ({ onFormSubmit }: FormInputProps) => {
    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            username: '',
            password: '',
            email: '',
            age: 0,
        },
        mode: 'onChange',
    });

    return (
        <FormProvider {...form}>
            <form onSubmit={form.handleSubmit(onFormSubmit)} className="flex w-full justify-center">
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
                    name="email"
                    label="Email"
                    type="email"
                    placeholder="Enter your email"
                />
                <InputComponent
                    control={form.control}
                    name="age"
                    label="Age"
                    type="number"
                    placeholder="Enter your age"
                />
                <Button type="submit" data-testid="submit">
                    Submit
                </Button>
            </form>
        </FormProvider>
    );
};

// Tests
describe('InputComponent', () => {
    it('shows required validation error for all fields', async () => {
        const handleSubmit = jest.fn();
        const { getByTestId, findAllByText } = render(<RenderInputComponent onFormSubmit={handleSubmit} />);

        const submitButton = getByTestId('submit'); // Find the submit button
        await userEvent.click(submitButton); // Click the submit button without filling out the input

        // Find all instances of the required error message
        const requiredErrors = await findAllByText(REQUIRED_MESSAGE); // Look for all 'Required' messages

        // Expect exactly 4 required error messages to be present (one for each input field)
        expect(requiredErrors).toHaveLength(3);

        // Ensure the form hasn't been submitted
        expect(handleSubmit).not.toHaveBeenCalled();
    });

    //username
    it('shows min length validation error', async () => {
        const handleSubmit = jest.fn();
        const { getByPlaceholderText, getByTestId, findByText } = render(
            <RenderInputComponent onFormSubmit={handleSubmit} />,
        );

        const input = getByPlaceholderText('Enter your username');
        const submitButton = getByTestId('submit');

        await userEvent.type(input, 'ab');
        await userEvent.click(submitButton);

        const minLengthError = await findByText(USERNAME_MIN_LENGTH_MESSAGE);
        expect(minLengthError).toBeInTheDocument();
        expect(handleSubmit).not.toHaveBeenCalled();
    });

    it('shows max length validation error', async () => {
        const handleSubmit = jest.fn();
        const { getByPlaceholderText, getByTestId, findByText } = render(
            <RenderInputComponent onFormSubmit={handleSubmit} />,
        );

        const input = getByPlaceholderText('Enter your username');
        const submitButton = getByTestId('submit');

        await userEvent.type(input, 'a'.repeat(16)); // 16 characters
        await userEvent.click(submitButton);

        const maxLengthError = await findByText(USERNAME_MAX_LENGTH_MESSAGE);
        expect(maxLengthError).toBeInTheDocument();
        expect(handleSubmit).not.toHaveBeenCalled();
    });

    it('shows invalid character validation error', async () => {
        const handleSubmit = jest.fn();
        const { getByPlaceholderText, getByTestId, findByText } = render(
            <RenderInputComponent onFormSubmit={handleSubmit} />,
        );

        const input = getByPlaceholderText('Enter your username');
        const submitButton = getByTestId('submit');

        await userEvent.type(input, '!!!!');
        await userEvent.click(submitButton);

        const regexError = await findByText(USERNAME_REGEX_MESSAGE);
        expect(regexError).toBeInTheDocument();
        expect(handleSubmit).not.toHaveBeenCalled();
    });

    // Email validation tests
    it('shows invalid email error', async () => {
        const handleSubmit = jest.fn();
        const { getByPlaceholderText, getByTestId, findByText } = render(
            <RenderInputComponent onFormSubmit={handleSubmit} />,
        );

        const emailInput = getByPlaceholderText('Enter your email');
        const submitButton = getByTestId('submit');

        await userEvent.type(emailInput, 'invalid-email');
        await userEvent.click(submitButton);

        const emailError = await findByText(EMAIL_INVALID_FORMAT_MESSAGE);
        expect(emailError).toBeInTheDocument();
        expect(handleSubmit).not.toHaveBeenCalled();
    });

    // Password validation tests
    it('shows password minimum length validation error', async () => {
        const handleSubmit = jest.fn();
        const { getByPlaceholderText, getByTestId, findByText } = render(
            <RenderInputComponent onFormSubmit={handleSubmit} />,
        );

        const passwordInput = getByPlaceholderText('Enter your password');
        const submitButton = getByTestId('submit');

        await userEvent.type(passwordInput, 'Pass1');
        await userEvent.click(submitButton);

        const minLengthError = await findByText(PASSWORD_MIN_LENGTH_MESSAGE);
        expect(minLengthError).toBeInTheDocument();
        expect(handleSubmit).not.toHaveBeenCalled();
    });

    it('shows password missing character validation errors', async () => {
        const handleSubmit = jest.fn();
        const { getByPlaceholderText, getByTestId, findByText } = render(
            <RenderInputComponent onFormSubmit={handleSubmit} />,
        );

        const passwordInput = getByPlaceholderText('Enter your password');
        const submitButton = getByTestId('submit');

        // Test missing special character
        await userEvent.clear(passwordInput);
        await userEvent.type(passwordInput, 'Password1');
        await userEvent.click(submitButton);
        const specialCharError = await findByText(PASSWORD_SPECIAL_CHAR_MESSAGE);
        expect(specialCharError).toBeInTheDocument();

        // Test missing number
        await userEvent.clear(passwordInput);
        await userEvent.type(passwordInput, 'Password@');
        await userEvent.click(submitButton);
        const numberError = await findByText(PASSWORD_NUMBER_MESSAGE);
        expect(numberError).toBeInTheDocument();
    });

    // Age validation tests
    it('shows age minimum validation error', async () => {
        const handleSubmit = jest.fn();
        const { getByPlaceholderText, getByTestId, findByText } = render(
            <RenderInputComponent onFormSubmit={handleSubmit} />,
        );

        const ageInput = getByPlaceholderText('Enter your age');
        const submitButton = getByTestId('submit');

        await userEvent.clear(ageInput);
        await userEvent.type(ageInput, '15'); // Below minimum age
        await userEvent.click(submitButton);

        const minAgeError = await findByText(AGE_MIN_MESSAGE);
        expect(minAgeError).toBeInTheDocument();
        expect(handleSubmit).not.toHaveBeenCalled();
    });

    it('shows age maximum validation error', async () => {
        const handleSubmit = jest.fn();
        const { getByPlaceholderText, getByTestId, findByText } = render(
            <RenderInputComponent onFormSubmit={handleSubmit} />,
        );

        const ageInput = getByPlaceholderText('Enter your age');
        const submitButton = getByTestId('submit');

        await userEvent.clear(ageInput);
        await userEvent.type(ageInput, '70'); // Above maximum age
        await userEvent.click(submitButton);

        const maxAgeError = await findByText(AGE_MAX_MESSAGE);
        expect(maxAgeError).toBeInTheDocument();
        expect(handleSubmit).not.toHaveBeenCalled();
    });

    it('submits successfully with valid input', async () => {
        const handleSubmit = jest.fn();
        const { getByPlaceholderText, getByTestId } = render(<RenderInputComponent onFormSubmit={handleSubmit} />);

        await userEvent.type(getByPlaceholderText('Enter your username'), 'ValidUser');
        await userEvent.type(getByPlaceholderText('Enter your password'), 'Strong@Pass1');
        await userEvent.type(getByPlaceholderText('Enter your email'), 'test@example.com');
        await userEvent.type(getByPlaceholderText('Enter your age'), '25');

        await userEvent.click(getByTestId('submit'));

        // Ensure form submission
        await waitFor(() => expect(handleSubmit).toHaveBeenCalledTimes(1));
        expect(handleSubmit).toHaveBeenCalledWith(
            expect.objectContaining({
                username: 'ValidUser',
                password: 'Strong@Pass1',
                email: 'test@example.com',
                age: 25,
            }),
            expect.anything(),
        );
    });
});
