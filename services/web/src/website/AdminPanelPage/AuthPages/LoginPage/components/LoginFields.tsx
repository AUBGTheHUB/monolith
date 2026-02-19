import { InputComponent } from '@/internalLibrary/InputComponent/InputComponent';
import { Control } from 'react-hook-form';
import { LoginFormData } from '../validation/validation';

type LoginFormFieldsProps = {
    control: Control<LoginFormData>;
};

export default function LoginFields({ control }: LoginFormFieldsProps) {
    return (
        <>
            <InputComponent
                control={control}
                name="username"
                label="Username"
                type="text"
                placeholder="Enter your username"
                labelClassName="text-white"
                inputClassName="bg-transparent text-[#A6AAB2] border border-[#233340] rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#A6AAB2]"
            />

            <InputComponent
                control={control}
                name="password"
                label="Password"
                type="password"
                placeholder="Enter your password"
                labelClassName="text-white"
                inputClassName="bg-transparent text-[#A6AAB2] border border-[#233340] rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#A6AAB2]"
            />
        </>
    );
}
