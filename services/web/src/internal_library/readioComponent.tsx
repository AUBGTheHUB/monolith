import { Control, FieldValues, Path } from 'react-hook-form';
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';

interface RadioButtonProps<T extends FieldValues> {
    control: Control<T>;
    name: Path<T>;
    options: { label: string; value: string }[];
    groupLabel?: string;
    groupClassName?: string;
    itemClassName?: string;
    labelClassName?: string;
    inputClassName?: string;
}

export const RadioButton = <T extends FieldValues>({
    control,
    name,
    options,
    groupLabel,
    groupClassName = '',
    itemClassName = '',
    labelClassName = '',
    inputClassName = '',
}: RadioButtonProps<T>) => {
    return (
        <FormField
            control={control}
            name={name}
            render={({ field, fieldState: { error } }) => (
                <FormItem className={`space-y-3 ${groupClassName}`}>
                    {groupLabel && <FormLabel>{groupLabel}</FormLabel>}
                    <FormControl>
                        <RadioGroup
                            onValueChange={field.onChange}
                            value={field.value}
                            className="flex flex-col space-y-2"
                        >
                            {options.map((option) => (
                                <FormItem key={option.value} className={`flex items-center space-x-3 ${itemClassName}`}>
                                    <FormControl>
                                        <RadioGroupItem value={option.value} className={inputClassName} />
                                    </FormControl>
                                    <FormLabel className={labelClassName}>{option.label}</FormLabel>{' '}
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
