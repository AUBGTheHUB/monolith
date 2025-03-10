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
    formControlClassName?: string;
    selectContentClassName?: string;
    items: DropdownItem[];
};

export function DropdownComponent<T extends FieldValues = FieldValues>({
    name,
    label,
    placeholder,
    dropdownLabelClassName,
    selectValueClassName,
    selectItemClassName,
    formControlClassName,
    selectContentClassName,
    items,
    control,
}: DropdownComponentProps<T>) {
    const effectiveSelectItemClassName = `${selectItemClassName ? selectItemClassName + ' ' : ''}cursor-pointer`;

    return (
        <FormField
            control={control}
            name={name}
            render={({ field }) => (
                <FormItem>
                    <FormLabel className={dropdownLabelClassName}>{label}</FormLabel>
                    <Select onValueChange={field.onChange} defaultValue={field.value}>
                        <FormControl className={formControlClassName}>
                            <SelectTrigger data-testid="trigger">
                                <SelectValue className={selectValueClassName} placeholder={placeholder} />
                            </SelectTrigger>
                        </FormControl>
                        <SelectContent className={selectContentClassName}>
                            <SelectGroup>
                                {items.map((item) => (
                                    <SelectItem
                                        className={effectiveSelectItemClassName}
                                        key={item.value}
                                        value={item.value}
                                        data-testid={`dropdown-item-${item.value}`}
                                    >
                                        {item.name}
                                    </SelectItem>
                                ))}
                            </SelectGroup>
                        </SelectContent>
                    </Select>
                    <div className="min-h-6 !mb-3">
                        <FormMessage />
                    </div>
                </FormItem>
            )}
        />
    );
}
