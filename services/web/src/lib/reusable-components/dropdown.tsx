import { Select, SelectContent, SelectGroup, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Control, FieldPath, FieldValues } from 'react-hook-form';

type DropdownItem = {
    name: string;
    value: string;
};

type DropdownComponentProps<T extends FieldValues = FieldValues> = {
    control: Control<T>;
    name: FieldPath<T>;
    label: string;
    placeholder: string;
    dropdownLabelClassName?: string;
    selectValueClassName?: string;
    selectItemClassName?: string;
    items: DropdownItem[];
};

export function DropdownComponent<T extends FieldValues = FieldValues>({
    name,
    label,
    placeholder,
    dropdownLabelClassName,
    selectValueClassName,
    selectItemClassName,
    items,
    control,
}: DropdownComponentProps<T>) {
    return (
        <FormField
            control={control}
            name={name}
            render={({ field }) => (
                <FormItem>
                    <FormLabel className={dropdownLabelClassName}>{label}</FormLabel>
                    <Select onValueChange={field.onChange} defaultValue={field.value}>
                        <FormControl>
                            <SelectTrigger>
                                <SelectValue className={selectValueClassName} placeholder={placeholder} />
                            </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                            <SelectGroup>
                                {items.map((item) => (
                                    <SelectItem className={selectItemClassName} key={item.value} value={item.value}>
                                        {item.name}
                                    </SelectItem>
                                ))}
                            </SelectGroup>
                        </SelectContent>
                    </Select>
                    <div className="min-h-6">
                        <FormMessage />
                    </div>
                </FormItem>
            )}
        />
    );
}
