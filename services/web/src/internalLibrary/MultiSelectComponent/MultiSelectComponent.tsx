import { Control, FieldValues, Path } from 'react-hook-form';
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { cn } from '@/lib/utils';
import { MultiSelect } from '@/components/ui/multi-select.tsx';

type MultiSelectComponentProps<T extends FieldValues> = {
    control: Control<T>;
    name: Path<T>;
    label: string;
    options: string[];
    placeholder?: string;
    formItemClassName?: string;
    labelClassName?: string;
    className?: string;
};

export const MultiSelectComponent = <T extends FieldValues>({
    control,
    name,
    label,
    options,
    placeholder,
    formItemClassName,
    labelClassName,
    className,
}: MultiSelectComponentProps<T>) => {
    return (
        <FormField
            control={control}
            name={name}
            render={({ field, fieldState: { error } }) => (
                <FormItem className={cn('space-y-3', formItemClassName)}>
                    <FormLabel className={labelClassName}>{label}</FormLabel>
                    <FormControl>
                        <MultiSelect
                            options={options}
                            // Fallback to empty array if value is null/undefined
                            selected={field.value || []}
                            onChange={(vals) => field.onChange(vals)}
                            placeholder={placeholder}
                            className={className}
                        />
                    </FormControl>
                    {/* Maintain consistent error height to match InputComponent */}
                    <div className="min-h-[24px] !mb-3">{error && <FormMessage>{error.message}</FormMessage>}</div>
                </FormItem>
            )}
        />
    );
};
