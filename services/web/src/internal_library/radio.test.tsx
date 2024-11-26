import { render } from '@testing-library/react';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm, FormProvider, SubmitHandler } from 'react-hook-form';
import { z } from 'zod';
import { RadioButton, RadioButtonProps } from './radioComponent';
import { Button } from '@/components/ui/button';
import userEvent from '@testing-library/user-event';

const REQUIRED_MESSAGE = 'This field is required';

const formSchema = z.object({
    select: z.string().min(1, { message: REQUIRED_MESSAGE }),
});

class ResizeObserver {
    observe() {}
    unobserve() {}
    disconnect() {}
}
global.ResizeObserver = ResizeObserver;

const commonProps: FormSelectProps = {
    name: 'select',
    options: [
        { label: 'All new messages', value: 'all' },
        { label: 'Direct messages and mentions', value: 'mentions' },
        { label: 'Nothing', value: 'none' },
    ],
    onFormSubmit: () => {},
};

type FormSelectProps = Omit<RadioButtonProps<z.infer<typeof formSchema>>, 'control'> & {
    onFormSubmit: SubmitHandler<z.infer<typeof formSchema>>;
};

const RenderSelectComponent = (props: FormSelectProps) => {
    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            select: '',
        },
        mode: 'all',
    });

    return (
        <FormProvider {...form}>
            <form onSubmit={form.handleSubmit(props.onFormSubmit)} className="flex w-full justify-center">
                <RadioButton control={form.control} {...props} />
                <Button type="submit" data-testid="submit">
                    Submit
                </Button>
            </form>
        </FormProvider>
    );
};

describe('SelectComponent', () => {
    it('renders and submits the form', async () => {
        const handleSubmit = jest.fn();

        const { getByTestId } = render(<RenderSelectComponent {...commonProps} onFormSubmit={handleSubmit} />);

        await userEvent.click(getByTestId('radio-mentions'));

        await userEvent.click(getByTestId('submit'));

        expect(handleSubmit).toHaveBeenCalledWith(expect.objectContaining({ select: 'mentions' }), expect.anything());

        expect(handleSubmit).toHaveBeenCalledTimes(1);
    });
});
