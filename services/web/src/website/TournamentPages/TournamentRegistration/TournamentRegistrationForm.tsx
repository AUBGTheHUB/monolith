import { FormProvider, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Button } from '@/components/ui/button';
import { registrationSchema, type TournamentRegistrationFormData } from './schema';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { useMutation } from '@tanstack/react-query';

import { fieldGridStyles, formBlurBgStyles, formCardStyles, submitButtonStyles } from './styles';
import TournamentRegistrationFields from './components/TournamentRegistrationFields';
import { registerParticipant } from './api';

type TournamentRegistrationFormProps = {
    isRegTeamsFull: boolean;
};

export default function TournamentRegistrationForm({ isRegTeamsFull }: TournamentRegistrationFormProps) {
    const defaultValues = {
        full_name: '',
        age: undefined,
        email: '',
        university: '',
        address: '',
        team_option: undefined,
        team_code: '',
        team_name: '',
        rank: '',
        primary_role: undefined,
        alternative_role: undefined,
        share_info_with_sponsors: undefined,
    };

    const form = useForm<TournamentRegistrationFormData>({
        resolver: zodResolver(registrationSchema),
        defaultValues: defaultValues,
    });

    const { control, handleSubmit } = form;

    const { mutate } = useMutation({
        mutationFn: registerParticipant,
        onSuccess: () => {
            toast.success('You have successfully signed up!', {
                position: 'top-right',
                className: 'bg-[#213a5a] text-[#a9ccf0] border border-[#c9a24a]',
            });
            form.reset();
        },
        onError: () => {
            toast.error('Something went wrong. Please try again.', { position: 'top-right' });
        },
    });

    const onSubmit = (data: TournamentRegistrationFormData) => {
        mutate(data);
    };

    return (
        <>
            <FormProvider {...form}>
                <form onSubmit={handleSubmit(onSubmit)} className={formCardStyles}>
                    <div className={formBlurBgStyles} />

                    <div className={fieldGridStyles}>
                        <TournamentRegistrationFields control={control} isRegTeamsFull={isRegTeamsFull} />
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
