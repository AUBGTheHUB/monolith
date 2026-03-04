import { Control } from 'react-hook-form';
import { InputComponent } from '@/internalLibrary/InputComponent/InputComponent.tsx';
import { RegisterFormData } from '../validation/validation.tsx';

type RegisterFormFieldsProps = {
    control: Control<RegisterFormData>;
};

export function SecondRegisterFields({ control }: RegisterFormFieldsProps) {
    return (
        <>
            <InputComponent
                control={control}
                name="position"
                label="Position"
                type="text"
                placeholder="Enter your position"
                labelClassName="text-white"
                inputClassName="bg-transparent text-[#A6AAB2] border border-[#233340] rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#A6AAB2]"
            />

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
                name="social_links.github"
                label="Github"
                type="text"
                formItemClassName="col-span-2"
                placeholder="Paste a link to your github profile"
                labelClassName="text-white"
                inputClassName="bg-transparent text-[#A6AAB2] border border-[#233340] rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#A6AAB2]"
            />

            <InputComponent
                control={control}
                name="social_links.linkedin"
                label="LinkedIn"
                type="text"
                formItemClassName="col-span-2"
                placeholder="Paste a link to your LinkedIn profile"
                labelClassName="text-white"
                inputClassName="bg-transparent text-[#A6AAB2] border border-[#233340] rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#A6AAB2]"
            />

            <InputComponent
                control={control}
                name="social_links.website"
                label="Website"
                type="text"
                formItemClassName="col-span-2"
                placeholder="Paste a link to your website"
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

            <InputComponent
                control={control}
                name="repeat_password"
                label="Repeat password"
                type="password"
                placeholder="Repeat your password"
                labelClassName="text-white"
                inputClassName="bg-transparent text-[#A6AAB2] border border-[#233340] rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#A6AAB2]"
            />
        </>
    );
}
