import { Control, FieldValues, Path } from 'react-hook-form';
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { cn } from '@/utils';

export type InputTypes = 'text' | 'email' | 'password' | 'number' | 'url';

type InputProps<T extends FieldValues> = {
    control: Control<T>;
    name: Path<T>;
    label: string;
    type: InputTypes;
    placeholder?: string;
    formItemClassName?: string;
    labelClassName?: string;
    inputClassName?: string;
    disabled?: boolean;
};

function handleInputChange(value: string, type: InputTypes): string | number {
    return type === 'number' ? +value : value;
}

function handleFieldChange(
    onChange: (value: string | number) => void,
    type: InputTypes,
): (e: React.ChangeEvent<HTMLInputElement>) => void {
    return (e) => {
        onChange(handleInputChange(e.target.value, type));
    };
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
    disabled,
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
                            disabled={disabled}
                            {...field}
                            type={type}
                            placeholder={placeholder}
                            className={cn(inputClassName)}
                            onChange={handleFieldChange(field.onChange, type)}
                            value={type === 'number' ? field.value || '' : field.value}
                        />
                    </FormControl>
                    <div className="min-h-[24px] !mb-3">{error && <FormMessage>{error.message}</FormMessage>}</div>
                </FormItem>
            )}
        />
    );
};
