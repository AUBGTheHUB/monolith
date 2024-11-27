import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { useForm, FormProvider } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { RadioComponent } from './RadioComponent';
import '@testing-library/jest-dom';

// Mock ResizeObserver to avoid errors in Jest
global.ResizeObserver = jest.fn().mockImplementation(() => ({
    observe: jest.fn(),
    unobserve: jest.fn(),
    disconnect: jest.fn(),
}));

const RADIO_OPTIONS = [
    { label: 'All new messages', value: 'all' },
    { label: 'Direct messages and mentions', value: 'mentions' },
    { label: 'Nothing', value: 'none' },
];

// Validation schema
const FormSchema = z.object({
    notificationPreference: z.string().min(1, { message: 'Please select a preference' }),
});

// Helper function for rendering the component
const renderWithForm = (onSubmit: jest.Mock) => {
    const TestForm = () => {
        const form = useForm({
            resolver: zodResolver(FormSchema),
            defaultValues: {
                notificationPreference: '',
            },
        });

        return (
            <FormProvider {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)}>
                    <RadioComponent
                        control={form.control}
                        name="notificationPreference"
                        options={RADIO_OPTIONS}
                        groupLabel="Notify me about..."
                    />
                    <button data-testid="submit">Submit</button>
                </form>
            </FormProvider>
        );
    };

    render(<TestForm />);
};

describe('RadioComponent', () => {
    it('submits the correct value when a radio button is selected', async () => {
        const mockSubmit = jest.fn();
        renderWithForm(mockSubmit);

        await userEvent.click(screen.getByTestId('radio-item-all'));
        await userEvent.click(screen.getByTestId('submit'));

        expect(mockSubmit).toHaveBeenCalledWith({ notificationPreference: 'all' }, expect.anything());
        expect(mockSubmit).toHaveBeenCalledTimes(1);
    });

    it('shows an error message when no option is selected', async () => {
        const mockSubmit = jest.fn();
        renderWithForm(mockSubmit);

        await userEvent.click(screen.getByTestId('submit'));

        expect(await screen.findByText(/Please select a preference/i)).toBeInTheDocument();
        expect(mockSubmit).not.toHaveBeenCalled();
    });

    it('clears the error message when a valid option is selected', async () => {
        const mockSubmit = jest.fn();
        renderWithForm(mockSubmit);

        // Trigger error by submitting without selection
        await userEvent.click(screen.getByTestId('submit'));
        expect(await screen.findByText(/Please select a preference/i)).toBeInTheDocument();

        // Select an option to clear the error
        await userEvent.click(screen.getByLabelText(/Nothing/i));
        expect(screen.queryByText(/Please select a preference/i)).not.toBeInTheDocument();
    });
});
