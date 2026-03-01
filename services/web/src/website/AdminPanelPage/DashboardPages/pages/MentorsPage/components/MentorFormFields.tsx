import { Control } from 'react-hook-form';
import { InputComponent } from '@/internalLibrary/InputComponent/InputComponent.tsx';
import { MentorFormData } from '../validation/validation.tsx';
import { MentorsFormFieldMessages as MESSAGES } from '../messages.tsx';

type MentorFormFieldProps = {
    control: Control<MentorFormData>;
};

export function MentorFormFields({ control }: MentorFormFieldProps) {
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
                placeholder={MESSAGES.PLACEHOLDERS.IMAGE}
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
