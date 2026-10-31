import { Control } from 'react-hook-form';
import { InputComponent } from '@/internalLibrary/InputComponent/InputComponent.tsx';
import { RadioComponent } from '@/internalLibrary/RadioComponent/RadioComponent.tsx';
import { AttendeeFormData } from '../validation/validation.tsx';
import { AttendeesFormFieldMessages as MESSAGES } from '../messages.tsx';

type AttendeeFormFieldsProps = {
    control: Control<AttendeeFormData>;
};

export function AttendeeFormFields({ control }: AttendeeFormFieldsProps) {
    return (
        <>
            <InputComponent
                control={control}
                name="name"
                label={MESSAGES.LABELS.NAME}
                placeholder={MESSAGES.PLACEHOLDERS.NAME}
                type="text"
            />
            <InputComponent
                control={control}
                name="email"
                label={MESSAGES.LABELS.EMAIL}
                placeholder={MESSAGES.PLACEHOLDERS.EMAIL}
                type="email"
            />
            <RadioComponent
                control={control}
                name="ticket_type"
                options={MESSAGES.TICKET_TYPE_OPTIONS}
                groupLabel={MESSAGES.LABELS.TICKET_TYPE}
                groupClassName="text-white"
                labelClassName="text-white"
            />
            <RadioComponent
                control={control}
                name="has_paid"
                options={MESSAGES.HAS_PAID_OPTIONS}
                groupLabel={MESSAGES.LABELS.HAS_PAID}
                groupClassName="text-white"
                labelClassName="text-white"
            />
        </>
    );
}
