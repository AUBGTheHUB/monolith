/**
 * Custom hook for judge form logic (reusable across Add and Edit pages)
 */

import { useState } from 'react';
import {
    JudgeFormData,
    JudgeFormErrors,
    validateJudgeField,
    validateJudgeForm,
    isJudgeFormValid,
} from '../lib/judges.validation';

export function useJudgeForm(initialData?: JudgeFormData) {
    // Form state
    const [formData, setFormData] = useState<JudgeFormData>(
        initialData || {
            name: '',
            companyName: '',
            imageUrl: '',
        },
    );

    // Validation errors state
    const [errors, setErrors] = useState<JudgeFormErrors>({
        name: '',
        companyName: '',
        imageUrl: '',
    });

    /**
     * Handles input field changes and validates in real-time
     */
    const handleChange = (field: keyof JudgeFormData, value: string) => {
        setFormData((prev) => ({ ...prev, [field]: value }));
        const error = validateJudgeField(field, value);
        setErrors((prev) => ({ ...prev, [field]: error }));
    };

    /**
     * Validates all fields and updates errors
     * @returns True if form is valid
     */
    const validate = (): boolean => {
        const newErrors = validateJudgeForm(formData);
        setErrors(newErrors);
        return isJudgeFormValid(newErrors);
    };

    /**
     * Resets form to initial state
     */
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
        setFormData, // For useEffect in Edit page
    };
}
