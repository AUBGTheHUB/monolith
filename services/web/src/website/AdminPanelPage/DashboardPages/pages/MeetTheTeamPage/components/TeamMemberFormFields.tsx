import { Control } from 'react-hook-form';
import { FormField, FormItem, FormLabel, FormControl, FormMessage } from '@/components/ui/form.tsx';
import { Input } from '@/components/ui/input.tsx';
import { MultiSelect } from '@/components/ui/multi-select.tsx';
import { AVAILABLE_DEPARTMENTS } from '../constants.tsx';
import { TeamMemberFormFieldMessages as MESSAGES } from '../messages.tsx';
import { TeamMemberFormData } from '../validation/validation.tsx';

interface TeamMemberFormFieldsProps {
    control: Control<TeamMemberFormData>;
}

export function TeamMemberFormFields({ control }: TeamMemberFormFieldsProps) {
    return (
        <div className="space-y-6">
            <FormField
                control={control}
                name="name"
                render={({ field }) => (
                    <FormItem>
                        <FormLabel>{MESSAGES.LABELS.NAME}</FormLabel>
                        <FormControl>
                            <Input placeholder={MESSAGES.PLACEHOLDERS.NAME} {...field} />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                )}
            />

            <FormField
                control={control}
                name="image"
                render={({ field }) => (
                    <FormItem>
                        <FormLabel>{MESSAGES.LABELS.IMAGE}</FormLabel>
                        <FormControl>
                            <Input placeholder={MESSAGES.PLACEHOLDERS.IMAGE} {...field} />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                )}
            />

            <FormField
                control={control}
                name="departments"
                render={({ field }) => (
                    <FormItem>
                        <FormLabel>{MESSAGES.LABELS.DEPARTMENTS}</FormLabel>
                        <FormControl>
                            <MultiSelect
                                options={AVAILABLE_DEPARTMENTS}
                                selected={field.value}
                                onChange={field.onChange}
                                placeholder={MESSAGES.PLACEHOLDERS.DEPARTMENTS}
                            />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                )}
            />
        </div>
    );
}
