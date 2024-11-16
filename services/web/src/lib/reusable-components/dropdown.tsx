import { Select, SelectContent, SelectGroup, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';

type dropdownInput = {
    name: string;
    value: string;
};

type DropdownComponentProps = {
    label: string;
    placeholder: string;
    className: string;
    items: dropdownInput[];
};

export function DropdownComponent({ label, placeholder, className, items }: DropdownComponentProps) {
    return (
        <FormField
            name="fruit"
            render={({ field }) => (
                <FormItem>
                    <FormLabel>{label}</FormLabel>
                    <Select onValueChange={field.onChange} defaultValue={field.value}>
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
