// import { FormProvider, useForm, useWatch } from 'react-hook-form';
// import { zodResolver } from '@hookform/resolvers/zod';
// import { z } from 'zod';
// import { Button } from '@/components/ui/button';
// import { InputComponent } from '@/internalLibrary/InputComponent/InputComponent';
// import { DropdownComponent } from '@/internalLibrary/DropdownComponent/DropdownComponent';
// import { formSchema } from './schema';
// import { CandidateForm, DEPARTMENTS_OPTIONS, Question } from './constants';
import { useEffect, useState } from 'react';
// import { useMutation } from '@tanstack/react-query';
// import { jwtDecode } from 'jwt-decode';
// import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
// import { Loader2 } from 'lucide-react';

// import { getQuestions, registerCandidate } from './api';
// import { RESEND_COOLDOWN_SECONDS } from './config';
// import { useCooldownTimer } from '@/helpers/useCooldownTimer.ts';
// import {
//     sectionHeadingStyles,
//     sectionDividerStyles,
//     fieldGridStyles,
//     submitButtonStyles,
//     errorTextStyles,
// } from './styles';
// import { MultiSelectComponent } from '@/internalLibrary/MultiSelectComponent/MultiSelectComponent.tsx';
// import { formCardStyles } from '@/website/RegistrationFormPage/RegistrationForm/styles.ts';
// interface CandidatesFormProps {
//     RegSwitch: boolean;
// }

// export default function CandidatesForm({ RegSwitch }: CandidatesFormProps) {
export default function CandidatesForm() {
    // const params = new URLSearchParams(window.location.search);
    // const token = params.get('jwt_token') ?? undefined;
    // const decodedToken = useMemo<DecodedToken | null>(() => (token ? jwtDecode<DecodedToken>(token) : null), [token]);

    // const [isSubmitted, setIsSubmitted] = useState(false);
    const [fadeIn, setFadeIn] = useState(false);
    // const cooldown = useCooldownTimer(RESEND_COOLDOWN_SECONDS);

    // const [questions, setQuestions] = useState<Question[]>([]);

    useEffect(() => {
        const timer = setTimeout(() => setFadeIn(true), 100);
        return () => clearTimeout(timer);
    }, []);

    // const {
    //     mutate,
    //     // data,
    //     // isPending,
    //     // isError,
    //     // error,
    // } = useMutation({
    //     mutationFn: (formData: CandidateForm) => registerCandidate(formData),
    //     retry: 1,
    //     onSuccess: () => {
    //         // setIsSubmitted(true);
    //         cooldown.start();
    //         toast.success('Application successful', {
    //             position: 'top-right',
    //             autoClose: 5000,
    //             hideProgressBar: false,
    //             closeOnClick: true,
    //             pauseOnHover: true,
    //             draggable: true,
    //             className: 'bg-white text-black border border-gray-200',
    //         });
    //     },
    // });

    // const form = useForm<z.infer<typeof formSchema>>({
    //     resolver: zodResolver(formSchema),
    //     defaultValues: {
    //         departments: [],
    //         generalQuestions: [],
    //         developmentQuestions: [],
    //         designQuestions: [],
    //         marketingQuestions: [],
    //         prQuestions: [],
    //         logisticsQuestions: [],
    //     },
    // });
    //
    // const departments = useWatch({
    //     control: form.control,
    //     name: 'departments',
    // });
    //
    // const onSubmit = (data: z.infer<typeof formSchema>) => {
    //     const payload: CandidateForm = {
    //         form: {
    //             departments: data.departments,
    //             generalQuestions: data.generalQuestions,
    //             developmentQuestions: data.developmentQuestions,
    //             designQuestions: data.designQuestions,
    //             marketingQuestions: data.marketingQuestions,
    //             prQuestions: data.prQuestions,
    //             logisticsQuestions: data.logisticsQuestions,
    //         },
    //     };
    //
    //     mutate(payload);
    // };

    // const isFormDisabled = isPending || isSubmitted;
    // const isFormDisabled = false;

    // useEffect(() => {
    //     getQuestions().then((res) => {
    //         const questionsData: Question[] = res.questions.map((q) => {
    //             return {
    //                 ...q,
    //                 answer: '',
    //             };
    //         });
    //         setQuestions(questionsData);
    //         form.reset({
    //             departments: [],
    //             generalQuestions: questionsData.filter((q) => q.question_type === 'GENERAL'),
    //             developmentQuestions: questionsData.filter((q) => q.question_type === 'DEVELOPMENT'),
    //             designQuestions: questionsData.filter((q) => q.question_type === 'DESIGN'),
    //             marketingQuestions: questionsData.filter((q) => q.question_type === 'MARKETING'),
    //             prQuestions: questionsData.filter((q) => q.question_type === 'PR'),
    //             logisticsQuestions: questionsData.filter((q) => q.question_type === 'LOGISTICS'),
    //         });
    //     });
    // }, [form]);

    // if (!RegSwitch) {
    //     return (
    //         <div
    //             className={`w-full flex flex-col items-center overflow-hidden font-mont bg-white relative text-gray-800 min-h-screen transition-opacity duration-1000 pt-24 ${fadeIn ? 'opacity-100' : 'opacity-0'}`}
    //         >
    //             <div className="w-11/12 sm:w-4/5 flex justify-center mb-10 mt-16 z-10">
    //                 <p className="text-black tracking-[0.5em] text-4xl sm:text-5xl font-light">REGISTER</p>
    //             </div>
    //             <div className="h-[45vh] flex w-[80%] justify-center items-center z-10">
    //                 <div className="bg-white/80 backdrop-blur-md h-full rounded-3xl w-full border border-gray-200 shadow-xl flex justify-center items-center font-mont text-2xl">
    //                     <p className="text-center p-5 text-gray-800">{registrationMessage}</p>
    //                 </div>
    //             </div>
    //         </div>
    //     );
    // }

    return (
        <div
            className={`w-full flex flex-col items-center overflow-x-hidden font-mont bg-[#fafafa] relative text-gray-800 min-h-screen transition-opacity duration-1000 pt-14 ${fadeIn ? 'opacity-100' : 'opacity-0'}`}
        >
            <div className="w-11/12 sm:w-4/5 flex justify-center mb-12 mt-16 z-10">
                <p className="text-gray-900 tracking-[0.4em] text-3xl sm:text-4xl font-medium uppercase">
                    APPLICATIONS ARE CLOSED!
                </p>
            </div>

            {/*<div className="flex justify-center w-full z-10">*/}
            {/*<FormProvider {...form}>*/}
            {/*    <form onSubmit={form.handleSubmit(onSubmit)} className={formCardStyles}>*/}
            {/*        <div>*/}
            {/*            <p className={`${sectionHeadingStyles} mt-4`}>General Questions</p>*/}
            {/*            <hr className={sectionDividerStyles} />*/}

            {/*            <div className={fieldGridStyles}>*/}
            {/*                {questions*/}
            {/*                    .filter((q) => q.question_type === 'GENERAL')*/}
            {/*                    .map((question, i) => {*/}
            {/*                        if (question.answer_type === 'TEXT')*/}
            {/*                            return (*/}
            {/*                                <InputComponent*/}
            {/*                                    key={question.prompt}*/}
            {/*                                    control={form.control}*/}
            {/*                                    name={`generalQuestions.${i}.answer`}*/}
            {/*                                    label={question.prompt}*/}
            {/*                                    type={'text'}*/}
            {/*                                />*/}
            {/*                            );*/}
            {/*                        else if (question.answer_type === 'SINGLE_CHOICE')*/}
            {/*                            return (*/}
            {/*                                <DropdownComponent*/}
            {/*                                    key={question.prompt}*/}
            {/*                                    control={form.control}*/}
            {/*                                    name={`generalQuestions.${i}.answer`}*/}
            {/*                                    label={question.prompt}*/}
            {/*                                    placeholder={''}*/}
            {/*                                    items={question.options.map((option) => ({*/}
            {/*                                        name: option,*/}
            {/*                                        value: option,*/}
            {/*                                    }))}*/}
            {/*                                />*/}
            {/*                            );*/}
            {/*                        else if (question.answer_type === 'MULTIPLE_CHOICE')*/}
            {/*                            return (*/}
            {/*                                <MultiSelectComponent*/}
            {/*                                    key={question.prompt}*/}
            {/*                                    control={form.control}*/}
            {/*                                    name={`generalQuestions.${i}.answer`}*/}
            {/*                                    label={question.prompt}*/}
            {/*                                    options={question.options}*/}
            {/*                                />*/}
            {/*                            );*/}
            {/*                    })}*/}

            {/*                <MultiSelectComponent*/}
            {/*                    control={form.control}*/}
            {/*                    name={`departments`}*/}
            {/*                    label={'Which department(s) would you like to apply for?'}*/}
            {/*                    options={DEPARTMENTS_OPTIONS.map((d) => d.label)}*/}
            {/*                />*/}
            {/*            </div>*/}
            {/*            {departments.includes('Development') && (*/}
            {/*                <div>*/}
            {/*                    <p className={`${sectionHeadingStyles} mt-4`}>Development questions</p>*/}

            {/*                    <hr className={sectionDividerStyles} />*/}

            {/*                    {questions*/}
            {/*                        .filter((q) => q.question_type === 'DEVELOPMENT')*/}
            {/*                        .map((question, i) => {*/}
            {/*                            if (question.answer_type === 'TEXT') {*/}
            {/*                                return (*/}
            {/*                                    <InputComponent*/}
            {/*                                        key={question.prompt}*/}
            {/*                                        control={form.control}*/}
            {/*                                        name={`developmentQuestions.${i}.answer`}*/}
            {/*                                        label={question.prompt}*/}
            {/*                                        type="text"*/}
            {/*                                    />*/}
            {/*                                );*/}
            {/*                            }*/}

            {/*                            if (question.answer_type === 'SINGLE_CHOICE') {*/}
            {/*                                return (*/}
            {/*                                    <DropdownComponent*/}
            {/*                                        key={question.prompt}*/}
            {/*                                        control={form.control}*/}
            {/*                                        name={`developmentQuestions.${i}.answer`}*/}
            {/*                                        label={question.prompt}*/}
            {/*                                        placeholder=""*/}
            {/*                                        items={question.options.map((option) => ({*/}
            {/*                                            name: option,*/}
            {/*                                            value: option,*/}
            {/*                                        }))}*/}
            {/*                                    />*/}
            {/*                                );*/}
            {/*                            }*/}

            {/*                            if (question.answer_type === 'MULTIPLE_CHOICE') {*/}
            {/*                                return (*/}
            {/*                                    <MultiSelectComponent*/}
            {/*                                        key={question.prompt}*/}
            {/*                                        control={form.control}*/}
            {/*                                        name={`developmentQuestions.${i}.answer`}*/}
            {/*                                        label={question.prompt}*/}
            {/*                                        options={question.options}*/}
            {/*                                    />*/}
            {/*                                );*/}
            {/*                            }*/}

            {/*                            return null;*/}
            {/*                        })}*/}
            {/*                </div>*/}
            {/*            )}*/}
            {/*            {departments.includes('Design') && (*/}
            {/*                <div>*/}
            {/*                    <p className={`${sectionHeadingStyles} mt-4`}>Design questions</p>*/}

            {/*                    <hr className={sectionDividerStyles} />*/}

            {/*                    {questions*/}
            {/*                        .filter((q) => q.question_type === 'DESIGN')*/}
            {/*                        .map((question, i) => {*/}
            {/*                            if (question.answer_type === 'TEXT') {*/}
            {/*                                return (*/}
            {/*                                    <InputComponent*/}
            {/*                                        key={question.prompt}*/}
            {/*                                        control={form.control}*/}
            {/*                                        name={`designQuestions.${i}.answer`}*/}
            {/*                                        label={question.prompt}*/}
            {/*                                        type="text"*/}
            {/*                                    />*/}
            {/*                                );*/}
            {/*                            }*/}

            {/*                            if (question.answer_type === 'SINGLE_CHOICE') {*/}
            {/*                                return (*/}
            {/*                                    <DropdownComponent*/}
            {/*                                        key={question.prompt}*/}
            {/*                                        control={form.control}*/}
            {/*                                        name={`designQuestions.${i}.answer`}*/}
            {/*                                        label={question.prompt}*/}
            {/*                                        placeholder=""*/}
            {/*                                        items={question.options.map((option) => ({*/}
            {/*                                            name: option,*/}
            {/*                                            value: option,*/}
            {/*                                        }))}*/}
            {/*                                    />*/}
            {/*                                );*/}
            {/*                            }*/}

            {/*                            if (question.answer_type === 'MULTIPLE_CHOICE') {*/}
            {/*                                return (*/}
            {/*                                    <MultiSelectComponent*/}
            {/*                                        key={question.prompt}*/}
            {/*                                        control={form.control}*/}
            {/*                                        name={`designQuestions.${i}.answer`}*/}
            {/*                                        label={question.prompt}*/}
            {/*                                        options={question.options}*/}
            {/*                                    />*/}
            {/*                                );*/}
            {/*                            }*/}

            {/*                            return null;*/}
            {/*                        })}*/}
            {/*                </div>*/}
            {/*            )}*/}
            {/*            {departments.includes('Marketing') && (*/}
            {/*                <div>*/}
            {/*                    <p className={`${sectionHeadingStyles} mt-4`}>Marketing questions</p>*/}

            {/*                    <hr className={sectionDividerStyles} />*/}

            {/*                    {questions*/}
            {/*                        .filter((q) => q.question_type === 'MARKETING')*/}
            {/*                        .map((question, i) => {*/}
            {/*                            if (question.answer_type === 'TEXT') {*/}
            {/*                                return (*/}
            {/*                                    <InputComponent*/}
            {/*                                        key={question.prompt}*/}
            {/*                                        control={form.control}*/}
            {/*                                        name={`marketingQuestions.${i}.answer`}*/}
            {/*                                        label={question.prompt}*/}
            {/*                                        type="text"*/}
            {/*                                    />*/}
            {/*                                );*/}
            {/*                            }*/}

            {/*                            if (question.answer_type === 'SINGLE_CHOICE') {*/}
            {/*                                return (*/}
            {/*                                    <DropdownComponent*/}
            {/*                                        key={question.prompt}*/}
            {/*                                        control={form.control}*/}
            {/*                                        name={`marketingQuestions.${i}.answer`}*/}
            {/*                                        label={question.prompt}*/}
            {/*                                        placeholder=""*/}
            {/*                                        items={question.options.map((option) => ({*/}
            {/*                                            name: option,*/}
            {/*                                            value: option,*/}
            {/*                                        }))}*/}
            {/*                                    />*/}
            {/*                                );*/}
            {/*                            }*/}

            {/*                            if (question.answer_type === 'MULTIPLE_CHOICE') {*/}
            {/*                                return (*/}
            {/*                                    <MultiSelectComponent*/}
            {/*                                        key={question.prompt}*/}
            {/*                                        control={form.control}*/}
            {/*                                        name={`marketingQuestions.${i}.answer`}*/}
            {/*                                        label={question.prompt}*/}
            {/*                                        options={question.options}*/}
            {/*                                    />*/}
            {/*                                );*/}
            {/*                            }*/}

            {/*                            return null;*/}
            {/*                        })}*/}
            {/*                </div>*/}
            {/*            )}*/}
            {/*            {departments.includes('PR') && (*/}
            {/*                <div>*/}
            {/*                    <p className={`${sectionHeadingStyles} mt-4`}>PR questions</p>*/}

            {/*                    <hr className={sectionDividerStyles} />*/}

            {/*                    {questions*/}
            {/*                        .filter((q) => q.question_type === 'PR')*/}
            {/*                        .map((question, i) => {*/}
            {/*                            if (question.answer_type === 'TEXT') {*/}
            {/*                                return (*/}
            {/*                                    <InputComponent*/}
            {/*                                        key={question.prompt}*/}
            {/*                                        control={form.control}*/}
            {/*                                        name={`prQuestions.${i}.answer`}*/}
            {/*                                        label={question.prompt}*/}
            {/*                                        type="text"*/}
            {/*                                    />*/}
            {/*                                );*/}
            {/*                            }*/}

            {/*                            if (question.answer_type === 'SINGLE_CHOICE') {*/}
            {/*                                return (*/}
            {/*                                    <DropdownComponent*/}
            {/*                                        key={question.prompt}*/}
            {/*                                        control={form.control}*/}
            {/*                                        name={`prQuestions.${i}.answer`}*/}
            {/*                                        label={question.prompt}*/}
            {/*                                        placeholder=""*/}
            {/*                                        items={question.options.map((option) => ({*/}
            {/*                                            name: option,*/}
            {/*                                            value: option,*/}
            {/*                                        }))}*/}
            {/*                                    />*/}
            {/*                                );*/}
            {/*                            }*/}

            {/*                            if (question.answer_type === 'MULTIPLE_CHOICE') {*/}
            {/*                                return (*/}
            {/*                                    <MultiSelectComponent*/}
            {/*                                        key={question.prompt}*/}
            {/*                                        control={form.control}*/}
            {/*                                        name={`prQuestions.${i}.answer`}*/}
            {/*                                        label={question.prompt}*/}
            {/*                                        options={question.options}*/}
            {/*                                    />*/}
            {/*                                );*/}
            {/*                            }*/}

            {/*                            return null;*/}
            {/*                        })}*/}
            {/*                </div>*/}
            {/*            )}*/}
            {/*            {departments.includes('Logistics') && (*/}
            {/*                <div>*/}
            {/*                    <p className={`${sectionHeadingStyles} mt-4`}>Logistics questions</p>*/}

            {/*                    <hr className={sectionDividerStyles} />*/}

            {/*                    {questions*/}
            {/*                        .filter((q) => q.question_type === 'LOGISTICS')*/}
            {/*                        .map((question, i) => {*/}
            {/*                            if (question.answer_type === 'TEXT') {*/}
            {/*                                return (*/}
            {/*                                    <InputComponent*/}
            {/*                                        key={question.prompt}*/}
            {/*                                        control={form.control}*/}
            {/*                                        name={`logisticsQuestions.${i}.answer`}*/}
            {/*                                        label={question.prompt}*/}
            {/*                                        type="text"*/}
            {/*                                    />*/}
            {/*                                );*/}
            {/*                            }*/}

            {/*                            if (question.answer_type === 'SINGLE_CHOICE') {*/}
            {/*                                return (*/}
            {/*                                    <DropdownComponent*/}
            {/*                                        key={question.prompt}*/}
            {/*                                        control={form.control}*/}
            {/*                                        name={`logisticsQuestions.${i}.prompt`}*/}
            {/*                                        label={question.prompt}*/}
            {/*                                        placeholder=""*/}
            {/*                                        items={question.options.map((option) => ({*/}
            {/*                                            name: option,*/}
            {/*                                            value: option,*/}
            {/*                                        }))}*/}
            {/*                                    />*/}
            {/*                                );*/}
            {/*                            }*/}

            {/*                            if (question.answer_type === 'MULTIPLE_CHOICE') {*/}
            {/*                                return (*/}
            {/*                                    <MultiSelectComponent*/}
            {/*                                        key={question.prompt}*/}
            {/*                                        control={form.control}*/}
            {/*                                        name={`logisticsQuestions.${i}.prompt`}*/}
            {/*                                        label={question.prompt}*/}
            {/*                                        options={question.options}*/}
            {/*                                    />*/}
            {/*                                );*/}
            {/*                            }*/}

            {/*                            return null;*/}
            {/*                        })}*/}
            {/*                </div>*/}
            {/*            )}*/}
            {/*        </div>*/}

            {/*        <div className="flex justify-center md:justify-start mt-8">*/}
            {/*            <Button*/}
            {/*                disabled={isFormDisabled}*/}
            {/*                type="submit"*/}
            {/*                className={`${submitButtonStyles} ${*/}
            {/*                    isFormDisabled ? 'opacity-50 cursor-not-allowed' : ''*/}
            {/*                }`}*/}
            {/*            >*/}
            {/*                {isPending ? (*/}
            {/*                    <>*/}
            {/*                        <Loader2 className="animate-spin mr-2" size={16} />*/}
            {/*                        Please wait*/}
            {/*                    </>*/}
            {/*                ) : (*/}
            {/*                    'Apply now'*/}
            {/*                )}*/}
            {/*            </Button>*/}
            {/*        </div>*/}

            {/*        {isError && error instanceof Error && <p className={errorTextStyles}>{error.message}</p>}*/}
            {/*    </form>*/}
            {/*</FormProvider>*/}
            {/*</div>*/}

            {/*<ToastContainer*/}
            {/*    position="top-right"*/}
            {/*    autoClose={5000}*/}
            {/*    hideProgressBar={false}*/}
            {/*    newestOnTop={false}*/}
            {/*    closeOnClick={true}*/}
            {/*    rtl={false}*/}
            {/*    pauseOnFocusLoss={true}*/}
            {/*    draggable={true}*/}
            {/*    pauseOnHover={true}*/}
            {/*/>*/}
        </div>
    );
}
