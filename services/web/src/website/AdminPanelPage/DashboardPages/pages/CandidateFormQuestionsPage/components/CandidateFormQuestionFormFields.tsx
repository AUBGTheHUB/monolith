import { Control } from 'react-hook-form';
import { InputComponent } from '@/internalLibrary/InputComponent/InputComponent.tsx';
import { CandidateFormQuestionFormData } from '../validation/validation.tsx';
import { CandidateFormQuestionFormFieldMessages as MESSAGES } from '../messages.tsx';
import { MultiSelectComponent } from '@/internalLibrary/MultiSelectComponent/MultiSelectComponent.tsx';
import { AVAILABLE_ANSWER_TYPES, AVAILABLE_QUESTION_TYPES } from '../constants.tsx';

type CandidateFormQuestionsFieldsProps = {
    control: Control<CandidateFormQuestionFormData>;
};

export function CandidateFormQuestionsFormFields({ control }: CandidateFormQuestionsFieldsProps) {
    return (
        <>
            <InputComponent
                control={control}
                name="prompt"
                label={MESSAGES.LABELS.PROMPT}
                placeholder={MESSAGES.PLACEHOLDERS.NAME}
                type="text"
            />
            <MultiSelectComponent
                control={control}
                name={'answer_type'}
                label={MESSAGES.LABELS.ANSWERTYPE}
                options={AVAILABLE_ANSWER_TYPES}
            />
            <MultiSelectComponent
                control={control}
                name={'question_type'}
                label={MESSAGES.LABELS.QUESTIONTYPE}
                options={AVAILABLE_QUESTION_TYPES}
            />
            {/* fix */}
            <InputComponent
                control={control}
                name="options"
                label={MESSAGES.LABELS.OPTIONS}
                placeholder={MESSAGES.PLACEHOLDERS.OPTIONS}
                type="text"
            />
        </>
    );
}
