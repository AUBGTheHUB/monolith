import { Control } from 'react-hook-form';
import { InputComponent } from '@/internalLibrary/InputComponent/InputComponent.tsx';
import { RegisterFormFields } from '../validation/validation.tsx';
import { DEPARTMENT_OPTIONS } from '../../../../../constants.ts';
import { MultiSelect } from '@/components/ui/multi-select.tsx';
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form.tsx';

type RegisterFormFieldsProps = {
    control: Control<RegisterFormFields>;
};

export function FirstRegisterFields({ control }: RegisterFormFieldsProps) {
    return (
        <>
            <InputComponent
                control={control}
                name="name"
                label="Name"
                type="text"
                placeholder="Enter your name"
                labelClassName="text-white"
                inputClassName="bg-transparent text-[#A6AAB2] border border-[#233340] rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#A6AAB2]"
            />

            <FormField
                control={control}
                name="departments"
                render={({ field }) => (
                    <FormItem>
                        <FormLabel>Department</FormLabel>
                        <FormControl>
                            <MultiSelect
                                options={DEPARTMENT_OPTIONS}
                                selected={field.value ?? []}
                                onChange={field.onChange}
                                placeholder="Choose a department"
                            />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                )}
            />
            {/* TODO: has to be changed to file */}
            <InputComponent
                control={control}
                name="avatar_url"
                label="Avatar Url"
                type="text"
                placeholder="Paste an avatar url"
                labelClassName="text-white"
                inputClassName="bg-transparent text-[#A6AAB2] border border-[#233340] rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#A6AAB2]"
            />
        </>
    );
}
