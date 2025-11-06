import { useState } from 'react';
import {
    JudgeFormData,
    JudgeFormErrors,
    validateJudgeField,
    validateJudgeForm,
    isJudgeFormValid,
} from '../lib/judges.validation';

export function useJudgeForm(initialData?: JudgeFormData) {
    const [formData, setFormData] = useState<JudgeFormData>(
        initialData || {
            name: '',
            companyName: '',
            imageUrl: '',
        },
    );

    const [errors, setErrors] = useState<JudgeFormErrors>({
        name: '',
        companyName: '',
        imageUrl: '',
    });

    const handleChange = (field: keyof JudgeFormData, value: string) => {
        setFormData((prev) => ({ ...prev, [field]: value }));
        const error = validateJudgeField(field, value);
        setErrors((prev) => ({ ...prev, [field]: error }));
    };

    const validate = (): boolean => {
        const newErrors = validateJudgeForm(formData);
        setErrors(newErrors);
        return isJudgeFormValid(newErrors);
    };

    const reset = () => {
        setFormData(
            initialData || {
                name: '',
                companyName: '',
                imageUrl: '',
            },
        );
        setErrors({
            name: '',
            companyName: '',
            imageUrl: '',
        });
    };

    return {
        formData,
        errors,
        handleChange,
        validate,
        reset,
        setFormData, 
    };
}
