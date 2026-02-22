import { Control, FieldValues, Path } from 'react-hook-form';
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { cn } from '@/lib/utils';

export type InputTypes = 'text' | 'email' | 'password' | 'number' | 'url' | 'file';
type InputValue = string | number | FileList | null;
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
    accept?: string;
};

// 2. Updated helper to handle FileList
function handleFieldChange(
    onChange: (value: InputValue) => void,
    type: InputTypes,
): (e: React.ChangeEvent<HTMLInputElement>) => void {
    return (e) => {
        if (type === 'file') {
            onChange(e.target.files); // Pass the FileList object
        } else {
            const value = e.target.value;
            onChange(type === 'number' ? +value : value);
        }
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
                            // 3. File inputs must NOT have a value prop (it throws a DOM exception)
                            value={type === 'file' ? undefined : type === 'number' ? field.value || '' : field.value}
                        />
                    </FormControl>
                    <div className="min-h-[24px] !mb-3">{error && <FormMessage>{error.message}</FormMessage>}</div>
                </FormItem>
            )}
        />
    );
};
