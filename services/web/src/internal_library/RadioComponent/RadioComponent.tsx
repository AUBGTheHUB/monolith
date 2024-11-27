import { Control, FieldValues, Path } from 'react-hook-form';
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { cn } from '@/lib/utils';

type Option = {
    label: string;
    value: string;
};

type RadioButtonProps<T extends FieldValues> = {
    control: Control<T>;
    name: Path<T>;
    options: Option[];
    groupLabel: string;
    groupClassName?: string;
    formItemClassName?: string;
    labelClassName?: string;
    radioGroupClassName?: string;
};

export const RadioComponent = <T extends FieldValues>({
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
                        <RadioGroup onValueChange={field.onChange} value={field.value} className={radioGroupClassName}>
                            {options.map((option) => (
                                <FormItem
                                    key={option.value}
                                    className={cn('flex items-center space-x-3 space-y-0', formItemClassName)}
                                >
                                    <FormControl>
                                        <RadioGroupItem
                                            value={option.value}
                                            className={radioGroupClassName}
                                            data-testid={`radio-item-${option.value}`}
                                        />
                                    </FormControl>
                                    <FormLabel className={labelClassName}>{option.label}</FormLabel>
                                </FormItem>
                            ))}
                        </RadioGroup>
                    </FormControl>
                    <div className="min-h-[24px]">{error && <FormMessage>{error.message}</FormMessage>}</div>
                </FormItem>
            )}
        />
    );
};
