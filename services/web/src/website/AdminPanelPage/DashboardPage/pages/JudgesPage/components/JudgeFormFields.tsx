import { Control } from 'react-hook-form';
import { InputComponent } from '@/internal_library/InputComponent/InputComponent';
import { JudgeFormData } from '../lib/judges.validation.tsx';

const MESSAGES = {
    LABELS: {
        NAME: 'Name',
        COMPANY: 'Company Name',
        IMAGE: 'Image URL',
    },
    PLACEHOLDERS: {
        NAME: "Enter judge's full name",
        COMPANY: 'Enter company name',
        IMAGE: 'Enter image URL (e.g., /judge_photo.webp)',
    },
};

type JudgeFormFieldsProps = {
    control: Control<JudgeFormData>;
};

export function JudgeFormFields({ control }: JudgeFormFieldsProps) {
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
                name="companyName"
                label={MESSAGES.LABELS.COMPANY}
                placeholder={MESSAGES.PLACEHOLDERS.COMPANY}
                type="text"
            />
            <InputComponent
                control={control}
                name="imageUrl"
                label={MESSAGES.LABELS.IMAGE}
                placeholder={MESSAGES.PLACEHOLDERS.IMAGE}
                type="text"
            />
        </>
    );
}
