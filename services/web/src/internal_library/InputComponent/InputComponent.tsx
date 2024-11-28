import { Control, FieldValues, Path } from 'react-hook-form';
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { cn } from '@/lib/utils';

type InputTypes = 'text' | 'email' | 'password' | 'number';

type InputProps<T extends FieldValues> = {
    control: Control<T>;
    name: Path<T>;
    label: string;
    type: InputTypes;
    placeholder?: string;
    formItemClassName?: string;
    labelClassName?: string;
    inputClassName?: string;
};

function handleInputChange(value: string, type: InputTypes): string | number {
    return type === 'number' ? +value : value;
}

export const InputComponent = <T extends FieldValues>({
    control,
    name,
    label,
    type,
    placeholder,
    formItemClassName,
    labelClassName,
    inputClassName,
}: InputProps<T>) => {
    return (
        <FormField
            control={control}
            name={name}
            render={({ field, fieldState: { error } }) => (
                <FormItem className={cn('space-y-3', formItemClassName)}>
                    <FormLabel className={labelClassName}>{label}</FormLabel>
                    <FormControl>
                        <Input
                            {...field}
                            type={type}
                            placeholder={placeholder}
                            className={cn(inputClassName)}
                            onChange={(e) => {
                                field.onChange(handleInputChange(e.target.value, type));
                            }}
                            value={type === 'number' ? field.value || '' : field.value}
                        />
                    </FormControl>
                    <div className="min-h-[24px]">{error && <FormMessage>{error.message}</FormMessage>}</div>
                </FormItem>
            )}
        />
    );
};
