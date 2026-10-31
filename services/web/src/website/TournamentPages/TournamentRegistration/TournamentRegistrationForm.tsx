import { FormProvider, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Button } from '@/components/ui/button';
import { registrationSchema, type TournamentRegistrationFormData } from './schema';

import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import { fieldGridStyles, submitButtonStyles } from './styles';
import TournamentRegistrationFields from './components/TournamentRegistrationFields';

export default function TournamentRegistrationForm() {
    const form = useForm<TournamentRegistrationFormData>({
        resolver: zodResolver(registrationSchema),
        defaultValues: {
            first_name: '',
            last_name: '',
            age: undefined,
            email: '',
            university: '',
            country: '',
            address: '',
            team_option: undefined,
            team_code: '',
            team_name: '',
            rank: '',
            primary_role: '',
            alternative_role: '',
            share_info_with_sponsors: undefined,
        },
    });

    const { control, handleSubmit } = form;

    const onSubmit = (data: TournamentRegistrationFormData) => {
        console.log('Form data:', data);
        toast.success('Form submitted', {
            position: 'top-right',
            autoClose: 5000,
            className: 'bg-[#213a5a] text-[#a9ccf0] border border-[#c9a24a]',
        });
    };

    return (
        <>
            <FormProvider {...form}>
                <form
                    onSubmit={handleSubmit(onSubmit)}
                    className="relative isolate w-full rounded-[20px] px-5 py-8 md:px-12 md:py-10 flex flex-col"
                >
                    <div className="absolute inset-0 -z-10 rounded-[20px] bg-[#163B59] blur-[20px]" />
                    <div className={fieldGridStyles}>
                        <TournamentRegistrationFields control={control} />
                    </div>

                    <div className="flex justify-end mt-8">
                        <Button type="submit" className={submitButtonStyles}>
                            SEND
                        </Button>
                    </div>
                </form>
            </FormProvider>
            <ToastContainer position="top-right" autoClose={5000} pauseOnHover draggable closeOnClick />
        </>
    );
}
