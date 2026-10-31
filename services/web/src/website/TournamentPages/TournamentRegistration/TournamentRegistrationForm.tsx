import { FormProvider, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Button } from '@/components/ui/button';
import { registrationSchema, type TournamentRegistrationFormData } from './schema';

import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import { fieldGridStyles, formBlurBgStyles, formCardStyles, submitButtonStyles } from './styles';
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
            primary_role: undefined,
            alternative_role: undefined,
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
                <form onSubmit={handleSubmit(onSubmit)} className={formCardStyles}>
                    <div className={formBlurBgStyles} />

                    <div className={fieldGridStyles}>
                        <TournamentRegistrationFields control={control} />
                    </div>

                    <div className="flex justify-end mt-[clamp(1.5rem,5vw,2.5rem)]">
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
