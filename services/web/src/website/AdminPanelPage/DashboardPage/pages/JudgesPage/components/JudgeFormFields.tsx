/**
 * Shared form components for judge forms
 */

import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';

const MESSAGES = {
    LABELS: {
        NAME: 'Name',
        COMPANY: 'Company Name',
        IMAGE: 'Image URL',
        REQUIRED: '*',
        PREVIEW: 'Preview:',
    },
    PLACEHOLDERS: {
        NAME: "Enter judge's full name",
        COMPANY: 'Enter company name',
        IMAGE: 'Enter image URL (e.g., /judge_photo.webp)',
    },
    HINTS: {
        NAME: '2-100 characters',
        COMPANY: '2-100 characters',
    },
};

type FormFieldProps = {
    id: string;
    label: string;
    placeholder: string;
    value: string;
    error: string;
    hint?: string;
    required?: boolean;
    onChange: (value: string) => void;
};

export function FormField({ id, label, placeholder, value, error, hint, required = false, onChange }: FormFieldProps) {
    return (
        <div className="space-y-2">
            <Label htmlFor={id} className="text-base">
                {label} {required && <span className="text-red-500">*</span>}
            </Label>
            <Input
                id={id}
                placeholder={placeholder}
                value={value}
                onChange={(e) => onChange(e.target.value)}
                className={error ? 'border-red-500' : ''}
            />
            {error && <p className="text-sm text-red-500">{error}</p>}
            {hint && <p className="text-xs text-gray-500">{hint}</p>}
        </div>
    );
}

type ImagePreviewProps = {
    url: string;
};

export function ImagePreview({ url }: ImagePreviewProps) {
    return (
        <div className="mt-4 p-4 bg-gray-50 rounded-lg">
            <p className="text-sm text-gray-600 mb-2">{MESSAGES.LABELS.PREVIEW}</p>
            <img
                src={url}
                alt="Preview"
                className="w-24 h-24 rounded-full object-cover"
                onError={(e) => {
                    e.currentTarget.src = 'https://via.placeholder.com/150?text=Invalid+URL';
                }}
            />
        </div>
    );
}

type JudgeFormFieldsProps = {
    formData: {
        name: string;
        companyName: string;
        imageUrl: string;
    };
    errors: {
        name: string;
        companyName: string;
        imageUrl: string;
    };
    onChange: (field: 'name' | 'companyName' | 'imageUrl', value: string) => void;
};

export function JudgeFormFields({ formData, errors, onChange }: JudgeFormFieldsProps) {
    return (
        <>
            {/* Name Field */}
            <FormField
                id="name"
                label={MESSAGES.LABELS.NAME}
                placeholder={MESSAGES.PLACEHOLDERS.NAME}
                value={formData.name}
                error={errors.name}
                hint={MESSAGES.HINTS.NAME}
                onChange={(value) => onChange('name', value)}
                required
            />

            {/* Company Name Field */}
            <FormField
                id="companyName"
                label={MESSAGES.LABELS.COMPANY}
                placeholder={MESSAGES.PLACEHOLDERS.COMPANY}
                value={formData.companyName}
                error={errors.companyName}
                hint={MESSAGES.HINTS.COMPANY}
                onChange={(value) => onChange('companyName', value)}
                required
            />

            {/* Image URL Field with Preview */}
            <div className="space-y-2">
                <Label htmlFor="imageUrl" className="text-base">
                    {MESSAGES.LABELS.IMAGE} <span className="text-red-500">{MESSAGES.LABELS.REQUIRED}</span>
                </Label>
                <Input
                    id="imageUrl"
                    placeholder={MESSAGES.PLACEHOLDERS.IMAGE}
                    value={formData.imageUrl}
                    onChange={(e) => onChange('imageUrl', e.target.value)}
                    className={errors.imageUrl ? 'border-red-500' : ''}
                />
                {errors.imageUrl && <p className="text-sm text-red-500">{errors.imageUrl}</p>}
                {formData.imageUrl && <ImagePreview url={formData.imageUrl} />}
            </div>
        </>
    );
}
