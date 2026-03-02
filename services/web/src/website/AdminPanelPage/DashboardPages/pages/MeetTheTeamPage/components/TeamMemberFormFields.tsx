import { Control } from 'react-hook-form';
import { TeamMemberFormFieldMessages as MESSAGES } from '../messages.tsx';
import { TeamMemberFormData } from '../validation/validation.tsx';
import { AVAILABLE_DEPARTMENTS } from '../constants.tsx';
import { InputComponent } from '@/internalLibrary/InputComponent/InputComponent.tsx';
import { MultiSelectComponent } from '@/internalLibrary/MultiSelectComponent/MultiSelectComponent.tsx';

interface TeamMemberFormFieldsProps {
    control: Control<TeamMemberFormData>;
}

export function TeamMemberFormFields({ control }: TeamMemberFormFieldsProps) {
    return (
        <>
            <InputComponent
                control={control}
                name={'name'}
                label={MESSAGES.LABELS.NAME}
                placeholder={MESSAGES.PLACEHOLDERS.NAME}
                type={'text'}
            />
            <InputComponent
                control={control}
                name={'position'}
                label={MESSAGES.LABELS.POSITION}
                placeholder={MESSAGES.PLACEHOLDERS.POSITION}
                type={'text'}
            />
            <InputComponent
                control={control}
                name="avatar"
                label={MESSAGES.LABELS.IMAGE}
                type="file"
                accept="image/*"
            />
            <MultiSelectComponent
                control={control}
                name={'departments'}
                label={MESSAGES.LABELS.DEPARTMENT}
                options={AVAILABLE_DEPARTMENTS}
            />
            <InputComponent
                control={control}
                name="social_links.linkedin"
                label={MESSAGES.LABELS.SOCIAL_LINKEDIN}
                type="url"
                placeholder={MESSAGES.PLACEHOLDERS.SOCIAL_LINKEDIN}
            />

            <InputComponent
                control={control}
                name="social_links.github"
                label={MESSAGES.LABELS.SOCIAL_GITHUB}
                type="url"
                placeholder={MESSAGES.PLACEHOLDERS.SOCIAL_GITHUB}
            />

            <InputComponent
                control={control}
                name="social_links.website"
                label={MESSAGES.LABELS.SOCIAL_WEBSITE}
                type="url"
                placeholder={MESSAGES.PLACEHOLDERS.SOCIAL_WEBSITE}
            />
        </>
    );
}
