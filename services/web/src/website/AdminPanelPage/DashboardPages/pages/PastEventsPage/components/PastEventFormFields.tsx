import { Control, Controller } from 'react-hook-form';
import { InputComponent } from '@/internalLibrary/InputComponent/InputComponent';
import { FormItem, FormControl, FormLabel, FormMessage } from '@/components/ui/form';
import { PastEventFormData } from '../validation/validation';
import { PastEventsFormFieldMessages as MESSAGES } from '../messages';
import { Badge } from '@/components/ui/badge';
import { useState } from 'react';
import { Styles } from '@/website/AdminPanelPage/AdminStyle';
import { cn } from '@/lib/utils.ts';

type PastEventFormFieldsProps = {
    control: Control<PastEventFormData>;
};

export function PastEventFields({ control }: PastEventFormFieldsProps) {
    const [tagInput, setTagInput] = useState('');

    return (
        <>
            <InputComponent
                control={control}
                name="title"
                label={MESSAGES.LABELS.TITLE}
                placeholder={MESSAGES.PLACEHOLDERS.TITLE}
                type="text"
            />

            <InputComponent
                control={control}
                name="image"
                label={MESSAGES.LABELS.IMAGE}
                placeholder={MESSAGES.PLACEHOLDERS.IMAGE}
                type="url"
            />

            <Controller
                control={control}
                name="tags"
                render={({ field: { value: tags = [], onChange }, fieldState: { error } }) => (
                    <FormItem className="space-y-3">
                        <FormLabel className="text-white">{MESSAGES.LABELS.TAGS}</FormLabel>
                        <FormControl>
                            <div className="flex flex-wrap items-center gap-2 border rounded-md px-3 py-2 bg-white focus-within:ring-2 focus-within:ring-white/40">
                                {tags.map((tag) => (
                                    <Badge
                                        key={tag}
                                        onClick={() => onChange(tags.filter((t) => t !== tag))}
                                        className={cn(
                                            'cursor-pointer hover:bg-gray-300 transition',
                                            Styles.backgrounds.primaryGradient,
                                        )}
                                    >
                                        {tag} ✕
                                    </Badge>
                                ))}

                                <input
                                    value={tagInput}
                                    placeholder="Type a tag and press Enter"
                                    className="flex-1 bg-white outline-none text-black placeholder-gray-400 min-w-[120px]"
                                    onChange={(e) => setTagInput(e.target.value)}
                                    onKeyDown={(e) => {
                                        if (e.key === 'Enter') {
                                            e.preventDefault();
                                            const trimmed = tagInput.trim();
                                            if (trimmed && !tags.includes(trimmed)) onChange([...tags, trimmed]);
                                            setTagInput('');
                                        }
                                    }}
                                />
                            </div>
                        </FormControl>
                        <div className="min-h-[24px] !mb-3">{error && <FormMessage>{error.message}</FormMessage>}</div>
                    </FormItem>
                )}
            />

            <InputComponent
                control={control}
                name="link"
                label={MESSAGES.LABELS.LINK}
                placeholder={MESSAGES.PLACEHOLDERS.LINK}
                type="url"
            />
        </>
    );
}
