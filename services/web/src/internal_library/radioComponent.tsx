import { Control, FieldValues, Path } from 'react-hook-form';
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { cn } from '@/lib/utils';

export type RadioButtonProps<T extends FieldValues> = {
    control: Control<T>;
    name: Path<T>;
    options: { label: string; value: string }[];
    groupLabel?: string;
    groupClassName?: string;
    formItemClassName?: string;
    labelClassName?: string;
    radioGroupClassName?: string;
};

export const RadioButton = <T extends FieldValues>({
    control,
    name,
    options,
    groupLabel,
    groupClassName,
    radioGroupClassName,
    labelClassName,
    formItemClassName,
}: RadioButtonProps<T>) => {
    return (
        <FormField
            control={control}
            name={name}
            render={({ field, fieldState: { error } }) => (
                <FormItem className={cn('space-y-3', groupClassName)}>
                    {groupLabel && <FormLabel>{groupLabel}</FormLabel>}
                    <FormControl>
                        <RadioGroup
                            onValueChange={field.onChange}
                            value={field.value}
                            className={cn('', radioGroupClassName)}
                        >
                            {options.map((option) => (
                                <FormItem
                                    key={option.value}
                                    className={cn('flex items-center space-x-3 space-y-0', formItemClassName)}
                                >
                                    <FormControl>
                                        <RadioGroupItem
                                            value={option.value}
                                            className={cn('', radioGroupClassName)}
                                            data-testid={`radio-${option.value}`}
                                        />
                                    </FormControl>
                                    <FormLabel className={cn('', labelClassName)}>{option.label}</FormLabel>{' '}
                                </FormItem>
                            ))}
                        </RadioGroup>
                    </FormControl>
                    {error && <FormMessage>{error.message}</FormMessage>}
                </FormItem>
            )}
        />
    );
};
