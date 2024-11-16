import { Select, SelectContent, SelectGroup, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Control, FieldPath, FieldValues } from 'react-hook-form';

type dropdownInput = {
    name: string;
    value: string;
};

type DropdownComponentProps<T extends FieldValues = FieldValues> = {
    control: Control<T>;
    name: FieldPath<T>;
    label: string;
    placeholder: string;
    className: string;
    items: dropdownInput[];
};

export function DropdownComponent<T extends FieldValues = FieldValues>({
    name,
    label,
    placeholder,
    className,
    items,
    control,
}: DropdownComponentProps<T>) {
    return (
        <FormField
            control={control}
            name={name}
            render={({ field }) => (
                <FormItem>
                    <FormLabel>{label}</FormLabel>
                    <Select onValueChange={field.onChange} defaultValue={field.value}>
                        <FormControl>
                            <SelectTrigger className={className}>
                                <SelectValue placeholder={placeholder} />
                            </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                            <SelectGroup>
                                {items.map((item: dropdownInput) => (
                                    <SelectItem key={item.value} value={item.value}>
                                        {item.name}
                                    </SelectItem>
                                ))}
                            </SelectGroup>
                        </SelectContent>
                    </Select>
                    <FormMessage />
                </FormItem>
            )}
        />
    );
}
/*
        <Select>
            <SelectTrigger className={className}>
                <SelectValue placeholder={placeholder} />
            </SelectTrigger>
            <SelectContent>
                <SelectGroup>
                    {items.map((item: dropdownInput) => (
                        <SelectItem key={item.value} value={item.value}>
                            {item.name}
                        </SelectItem>
                    ))}
                </SelectGroup>
            </SelectContent>
        </Select>

*/
