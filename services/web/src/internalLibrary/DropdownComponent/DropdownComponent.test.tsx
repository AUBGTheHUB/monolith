import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import { DropdownComponent } from './DropdownComponent';

import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { z } from 'zod';

import { Button } from '@/components/ui/button';
import { Form } from '@/components/ui/form';

// Mock ResizeObserver to avoid errors in Jest
global.ResizeObserver = jest.fn().mockImplementation(() => ({
    observe: jest.fn(),
    unobserve: jest.fn(),
    disconnect: jest.fn(),
}));

window.HTMLElement.prototype.hasPointerCapture = jest.fn();
window.HTMLElement.prototype.scrollIntoView = jest.fn();

// Validation schema
const FormSchema = z.object({
    fruit: z.string().min(1, { message: 'Please select a fruit' }),
});

// Helper function for rendering the component
const renderWithForm = (onSubmit: jest.Mock) => {
    const TestForm = () => {
        const form = useForm({
            resolver: zodResolver(FormSchema),
            defaultValues: {
                fruit: '',
            },
            mode: 'onTouched',
        });

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
                    <Button data-testid="submit" type="submit">
                        Submit
                    </Button>
                </form>
            </Form>
        );
    };

    render(<TestForm />);
};

describe('DropdownComponent', () => {
    it('submits the correct value when the first dropdown item is selected', async () => {
        const mockSubmit = jest.fn();
        renderWithForm(mockSubmit);

        await userEvent.click(screen.getByTestId('trigger'));
        await userEvent.keyboard('[ArrowDown]');
        await userEvent.keyboard('[Enter]');
        // await userEvent.click(screen.getByTestId('dropdown-item-apple'));
        await userEvent.click(screen.getByTestId('submit'));

        expect(mockSubmit).toHaveBeenCalledWith({ fruit: 'banana' }, expect.anything());
        expect(mockSubmit).toHaveBeenCalledTimes(1);
    });

    it('submits the correct value when the second dropdown item is selected', async () => {
        const mockSubmit = jest.fn();
        renderWithForm(mockSubmit);

        await userEvent.click(screen.getByTestId('trigger'));
        await userEvent.keyboard('[Enter]');
        await userEvent.click(screen.getByTestId('submit'));

        expect(mockSubmit).toHaveBeenCalledWith({ fruit: 'apple' }, expect.anything());
        expect(mockSubmit).toHaveBeenCalledTimes(1);
    });
    it('shows an error message when no item is selected', async () => {
        const mockSubmit = jest.fn();
        renderWithForm(mockSubmit);

        await userEvent.click(screen.getByTestId('submit'));

        expect(await screen.findByText(/Please select a fruit/i)).toBeInTheDocument();
        expect(mockSubmit).not.toHaveBeenCalled();
    });

    it('clears the error message when a valid item is selected', async () => {
        const mockSubmit = jest.fn();
        renderWithForm(mockSubmit);

        // Trigger error by submitting without selection
        await userEvent.click(screen.getByTestId('submit'));
        expect(await screen.findByText(/Please select a fruit/i)).toBeInTheDocument();

        // Select the first option to clear the error
        await userEvent.click(screen.getByTestId('trigger'));
        await userEvent.keyboard('[Enter]');
        await userEvent.click(screen.getByTestId('submit'));
        expect(screen.queryByText(/Please select a fruit/i)).not.toBeInTheDocument();
    });
});
