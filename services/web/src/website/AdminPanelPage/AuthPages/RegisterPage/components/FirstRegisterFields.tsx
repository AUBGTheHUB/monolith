import { Control } from 'react-hook-form';
import { InputComponent } from '@/internalLibrary/InputComponent/InputComponent.tsx';
import { RegisterFormData } from '../validation/validation.tsx';
import { DropdownComponent } from '@/internalLibrary/DropdownComponent/DropdownComponent.tsx';
import { DEPARTMENT_OPTIONS } from '../constants.ts';

type RegisterFormFieldsProps = {
    control: Control<RegisterFormData>;
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

            <DropdownComponent
                control={control}
                name="department"
                label="Department"
                placeholder="Select your department"
                dropdownLabelClassName="text-white"
                selectContentClassName="bg-[#000912] text-white border border-[#233340]"
                formControlClassName="bg-[#000912] border border-[#233340]"
                items={DEPARTMENT_OPTIONS.map(({ label, value }) => ({ name: label, value }))}
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
