/**
 * Shared validation logic for judge forms
 */

// Validation constraints
export const JUDGE_VALIDATION_RULES = {
    NAME: {
        MIN_LENGTH: 2,
        MAX_LENGTH: 100,
    },
    COMPANY: {
        MIN_LENGTH: 2,
        MAX_LENGTH: 100,
    },
};

// Error messages
export const JUDGE_VALIDATION_ERRORS = {
    NAME_REQUIRED: 'Name is required',
    NAME_TOO_SHORT: `Name must be at least ${JUDGE_VALIDATION_RULES.NAME.MIN_LENGTH} characters`,
    NAME_TOO_LONG: `Name must be less than ${JUDGE_VALIDATION_RULES.NAME.MAX_LENGTH} characters`,
    COMPANY_REQUIRED: 'Company name is required',
    COMPANY_TOO_SHORT: `Company name must be at least ${JUDGE_VALIDATION_RULES.COMPANY.MIN_LENGTH} characters`,
    COMPANY_TOO_LONG: `Company name must be less than ${JUDGE_VALIDATION_RULES.COMPANY.MAX_LENGTH} characters`,
    IMAGE_REQUIRED: 'Image URL is required',
};

// Form data type
export type JudgeFormData = {
    name: string;
    companyName: string;
    imageUrl: string;
};

export type JudgeFormErrors = {
    name: string;
    companyName: string;
    imageUrl: string;
};

/**
 * Validates a single judge form field
 * @param field - The field name to validate
 * @param value - The current value of the field
 * @returns Error message string (empty if valid)
 */
export function validateJudgeField(field: keyof JudgeFormData, value: string): string {
    const trimmedValue = value.trim();

    switch (field) {
        case 'name':
            if (!trimmedValue) return JUDGE_VALIDATION_ERRORS.NAME_REQUIRED;
            if (trimmedValue.length < JUDGE_VALIDATION_RULES.NAME.MIN_LENGTH) {
                return JUDGE_VALIDATION_ERRORS.NAME_TOO_SHORT;
            }
            if (trimmedValue.length > JUDGE_VALIDATION_RULES.NAME.MAX_LENGTH) {
                return JUDGE_VALIDATION_ERRORS.NAME_TOO_LONG;
            }
            return '';

        case 'companyName':
            if (!trimmedValue) return JUDGE_VALIDATION_ERRORS.COMPANY_REQUIRED;
            if (trimmedValue.length < JUDGE_VALIDATION_RULES.COMPANY.MIN_LENGTH) {
                return JUDGE_VALIDATION_ERRORS.COMPANY_TOO_SHORT;
            }
            if (trimmedValue.length > JUDGE_VALIDATION_RULES.COMPANY.MAX_LENGTH) {
                return JUDGE_VALIDATION_ERRORS.COMPANY_TOO_LONG;
            }
            return '';

        case 'imageUrl':
            if (!trimmedValue) return JUDGE_VALIDATION_ERRORS.IMAGE_REQUIRED;
            return '';

        default:
            return '';
    }
}

/**
 * Validates all judge form fields at once
 * @param formData - The form data to validate
 * @returns Object containing all errors
 */
export function validateJudgeForm(formData: JudgeFormData): JudgeFormErrors {
    return {
        name: validateJudgeField('name', formData.name),
        companyName: validateJudgeField('companyName', formData.companyName),
        imageUrl: validateJudgeField('imageUrl', formData.imageUrl),
    };
}

/**
 * Checks if the form has any errors
 * @param errors - The errors object
 * @returns True if form is valid, false if there are errors
 */
export function isJudgeFormValid(errors: JudgeFormErrors): boolean {
    return !errors.name && !errors.companyName && !errors.imageUrl;
}
