'use client';

import { FormProvider, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Label } from '@/components/ui/label';
import { InputComponent } from '@/internalLibrary/InputComponent/InputComponent';
import { PastEventFormValues, pastEventSchema } from './schema';
import { Controller } from 'react-hook-form';

interface PastEventFormProps {
    defaultValues?: Partial<PastEventFormValues>;
    onSubmit: (data: PastEventFormValues) => void;
    submitLabel?: string;
}

export const PastEventForm = ({ defaultValues, onSubmit, submitLabel = 'Save' }: PastEventFormProps) => {
    const form = useForm<PastEventFormValues>({
        resolver: zodResolver(pastEventSchema),
        defaultValues: {
            title: defaultValues?.title || '',
            image: defaultValues?.image ?? undefined,
            tags: defaultValues?.tags || [],
            link: defaultValues?.link || '',
        },
        mode: 'onSubmit',
    });

    const {
        control,
        handleSubmit,
        setValue,
        watch,
        formState: { errors },
    } = form;

    const tags = watch('tags');
    const [tagInput, setTagInput] = useState('');

    const addTag = () => {
        const value = tagInput.trim();
        if (!value || tags.includes(value)) return;

        setValue('tags', [...tags, value], {
            shouldDirty: true,
            shouldValidate: true,
        });

        setTagInput('');
    };

    const removeTag = (tag: string) => {
        setValue(
            'tags',
            tags.filter((t) => t !== tag),
            {
                shouldDirty: true,
                shouldValidate: true,
            },
        );
    };

    return (
        <FormProvider {...form}>
            <form onSubmit={handleSubmit(onSubmit)} className="max-w-xl w-full space-y-5">
                <InputComponent
                    control={control}
                    name="title"
                    label="Name"
                    type="text"
                    placeholder="Event name"
                    labelClassName="text-white"
                    inputClassName="bg-transparent text-white border border-gray-500 rounded-md px-3 py-2"
                />
                <div>
                    <Label className="text-white mb-1.5 block">Event Image</Label>
                    <Controller
                        control={control}
                        name="image"
                        render={({ field: { onChange, value } }) => {
                            // Logic to determine what text to show
                            let displayName = 'Click to upload event image';

                            if (value instanceof File) {
                                displayName = value.name;
                            } else if (typeof value === 'string' && value !== '') {
                                // Extract filename from URL (e.g., /uploads/my-pic.jpg -> my-pic.jpg)
                                displayName = value.split('/').pop() || value;
                            }

                            return (
                                <label
                                    htmlFor="file-upload"
                                    className="flex items-center justify-between w-full bg-white/5 text-white border border-gray-500 rounded-md px-3 py-2 cursor-pointer hover:bg-white/10 hover:border-white/40 active:scale-[0.98] transition-all duration-200 group"
                                >
                                    <span
                                        className={`truncate text-sm ${!value ? 'text-gray-400' : 'text-white font-medium'}`}
                                    >
                                        {displayName}
                                    </span>

                                    {/* Upload Icon */}
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        width="18"
                                        height="18"
                                        viewBox="0 0 24 24"
                                        fill="none"
                                        stroke="currentColor"
                                        strokeWidth="2"
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        className="text-gray-500 group-hover:text-white transition-colors"
                                    >
                                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                                        <polyline points="17 8 12 3 7 8" />
                                        <line x1="12" x2="12" y1="3" y2="15" />
                                    </svg>

                                    <input
                                        id="file-upload"
                                        type="file"
                                        accept="image/*"
                                        className="hidden"
                                        onChange={(e) => {
                                            const file = e.target.files?.[0];
                                            if (file) onChange(file);
                                        }}
                                    />
                                </label>
                            );
                        }}
                    />
                    {errors.image && <p className="text-sm text-red-500 mt-1">{errors.image.message as string}</p>}
                </div>
                <div>
                    <Label className="text-white">Tags</Label>

                    <div className="flex flex-wrap items-center gap-2 border rounded-md px-3 py-2 bg-transparent focus-within:ring-2 focus-within:ring-white/40">
                        {tags.map((tag) => (
                            <Badge
                                key={tag}
                                onClick={() => removeTag(tag)}
                                className="cursor-pointer bg-white/10 text-white hover:bg-white/20 transition"
                                variant="secondary"
                            >
                                {tag} ✕
                            </Badge>
                        ))}

                        <input
                            value={tagInput}
                            placeholder="Type a tag and press Enter"
                            className="flex-1 bg-transparent outline-none text-white placeholder-gray-400 min-w-[120px]"
                            onChange={(e) => setTagInput(e.target.value)}
                            onKeyDown={(e) => {
                                if (e.key === 'Enter') {
                                    e.preventDefault();
                                    addTag();
                                }
                            }}
                        />
                    </div>

                    {errors.tags && <p className="text-sm text-red-500 mt-1">{errors.tags.message}</p>}
                </div>
                <InputComponent
                    control={control}
                    name="link"
                    label="Link (optional)"
                    type="text"
                    placeholder="https://thehub-aubg.com/events/example"
                    labelClassName="text-white"
                    inputClassName="bg-transparent text-white border border-gray-500 rounded-md px-3 py-2"
                />
                <Button type="submit" className="border border-white">
                    {submitLabel}
                </Button>
            </form>
        </FormProvider>
    );
};
