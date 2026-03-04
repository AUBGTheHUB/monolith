import { Control } from 'react-hook-form';
import { InputComponent } from '@/internalLibrary/InputComponent/InputComponent.tsx';
import { JudgeFormData } from '../validation/validation.tsx';
import { JudgesFormFieldMessages as MESSAGES } from '../messages.tsx';

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
                name="company"
                label={MESSAGES.LABELS.COMPANY}
                placeholder={MESSAGES.PLACEHOLDERS.COMPANY}
                type="text"
            />
            <InputComponent
                control={control}
                name="avatar"
                label={MESSAGES.LABELS.IMAGE}
                type="file"
                accept="image/*"
            />
            <InputComponent
                control={control}
                name="job_title"
                label={MESSAGES.LABELS.POSITION}
                placeholder={MESSAGES.PLACEHOLDERS.POSITION}
                type="text"
            />
            <InputComponent
                control={control}
                name="linkedin_url"
                label={MESSAGES.LABELS.LINKEDIN}
                placeholder={MESSAGES.PLACEHOLDERS.LINKEDIN}
                type="url"
            />
        </>
    );
}
