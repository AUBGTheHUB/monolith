import { Fragment, useEffect, useMemo } from 'react';
import { useParams, useNavigate } from 'react-router';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card.tsx';
import { Button } from '@/components/ui/button.tsx';
import { Helmet } from 'react-helmet';
import { TeamMemberEditMessages, TeamMemberAddMessages } from './messages.tsx';
import { Form } from '@/components/ui/form.tsx';
import { createTeamMemberSchema, TeamMemberFormData, updateTeamMemberSchema } from './validation/validation.tsx';
import { HubMember } from '@/types/hub-member.ts';
import { TeamMemberFormFields } from './components/TeamMemberFormFields.tsx';
import { Styles } from '../../../AdminStyle.ts';
import { cn } from '@/lib/utils.ts';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/services/apiClient.ts';
import { toFormData } from '@/helpers/formHelpers.ts';

export function MeetTheTeamEditPage() {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const queryClient = useQueryClient();

    const isEditMode = Boolean(id);
    const MESSAGES = isEditMode ? TeamMemberEditMessages : TeamMemberAddMessages;
    const schema = isEditMode ? updateTeamMemberSchema : createTeamMemberSchema;
    const form = useForm<TeamMemberFormData>({
        resolver: zodResolver(schema),
        defaultValues: {
            name: '',
            position: '',
            departments: [],
            avatar: undefined,
            social_links: {
                linkedin: '',
                github: '',
                website: '',
            },
        },
        mode: 'onTouched',
    });

    // 1. Fetch data if in Edit Mode
    const { data: member, isLoading } = useQuery({
        queryKey: ['hub-member', id],
        queryFn: () => apiClient.get<{ hub_member: HubMember }>(`/admin/hub-members/${id}`),
        enabled: isEditMode,
        select: (res) => res.hub_member,
    });
    const { control, handleSubmit, reset, watch } = form;
    // Watch the logo field (which is now a FileList)
    const avatarFile = watch('avatar');

    // Create a local preview URL
    const previewUrl = useMemo(() => {
        // 1. If user just selected a NEW file, show that preview
        if (avatarFile instanceof FileList && avatarFile.length > 0) {
            return URL.createObjectURL(avatarFile[0]);
        }

        // 2. Fallback to the existing sponsor logo from the database
        if (isEditMode && member?.avatar_url) {
            return member.avatar_url;
        }

        return null;
    }, [avatarFile, member, isEditMode]);

    // 2. Fill form when data is received
    useEffect(() => {
        if (member) {
            reset({
                name: member.name,
                position: member.position,
                departments: member.departments as ('Development' | 'Marketing' | 'Logistics' | 'PR' | 'Design')[],
                avatar: undefined,
                social_links: {
                    linkedin: member.social_links?.linkedin || '',
                    github: member.social_links?.github || '',
                    website: member.social_links?.website || '',
                },
            });
        }
    }, [member, reset]);

    // 3. Mutation for Save (Create or Update)
    const mutation = useMutation({
        mutationFn: (formData: FormData) => {
            return isEditMode
                ? apiClient.patchForm<HubMember>(`/admin/hub-members/${id}`, formData)
                : apiClient.postForm<HubMember>(`/admin/hub-members`, formData);
        },
        onSuccess: async () => {
            await queryClient.invalidateQueries({ queryKey: ['hub-members'] });
            navigate('/admin/dashboard/meet-the-team');
        },
        onError: (error: Error) => {
            alert(error.message);
        },
    });

    const onSubmit = (data: TeamMemberFormData) => {
        //Remove empty social links because API will otherwise replace them with empty strings
        data.social_links = Object.fromEntries(Object.entries(data.social_links).filter(([, value]) => !!value));

        const formData = toFormData(data);
        mutation.mutate(formData);
    };

    const goBack = () => {
        navigate('/admin/dashboard/meet-the-team');
    };

    const pageWrapperClass = cn('min-h-screen p-8', Styles.backgrounds.primaryGradient);

    if (isEditMode && isLoading) {
        return (
            <div className={pageWrapperClass}>
                <div className="max-w-5xl mx-auto text-white text-center py-20">
                    {TeamMemberEditMessages.LOADING_STATE}
                </div>
            </div>
        );
    }

    if (isEditMode && !member) {
        return (
            <Fragment>
                <Helmet>
                    <title>{TeamMemberEditMessages.NOT_FOUND_TITLE}</title>
                </Helmet>
                <div className={pageWrapperClass}>
                    <div className="max-w-2xl mx-auto">
                        <Card className={cn('p-12 text-center', Styles.glass.card)}>
                            <p className="text-red-400 text-lg mb-6">{TeamMemberEditMessages.NOT_FOUND_MESSAGE}</p>
                            <Button
                                style={{ backgroundColor: Styles.colors.hubCyan }}
                                className="text-white hover:opacity-90 transition-opacity"
                                onClick={goBack}
                            >
                                {TeamMemberEditMessages.RETURN_BUTTON}
                            </Button>
                        </Card>
                    </div>
                </div>
            </Fragment>
        );
    }

    return (
        <Fragment>
            <Helmet>
                <title>{MESSAGES.PAGE_TITLE}</title>
            </Helmet>

            <div className={pageWrapperClass}>
                <div className="max-w-5xl mx-auto">
                    <Button variant="ghost" onClick={goBack} className={cn('mb-4', Styles.glass.ghostButton)}>
                        {MESSAGES.BACK_BUTTON}
                    </Button>

                    <Card className={Styles.glass.card}>
                        <CardHeader className="border-b border-white/5 pb-8">
                            <CardTitle className={cn('text-3xl', Styles.text.title)}>{MESSAGES.HEADING}</CardTitle>
                            <p className={Styles.text.subtitle}>{MESSAGES.SUBTITLE}</p>
                        </CardHeader>

                        <Form {...form}>
                            <form onSubmit={handleSubmit(onSubmit)}>
                                <CardContent className="flex flex-col md:flex-row gap-12 p-8">
                                    <div className={cn('flex-1 space-y-6', Styles.forms.fieldContainer)}>
                                        <div className="form-dark-theme">
                                            <TeamMemberFormFields control={control} />
                                        </div>
                                    </div>

                                    <div className="flex-1 flex flex-col items-center justify-start gap-4 pt-8 md:pt-0">
                                        <span className={cn('self-start !text-white', Styles.text.label)}>
                                            Avatar Preview
                                        </span>
                                        <div
                                            className={cn(
                                                'relative w-full max-w-[400px] aspect-square rounded-lg flex items-center justify-center overflow-hidden',
                                                Styles.backgrounds.previewBox,
                                            )}
                                        >
                                            {previewUrl ? (
                                                <img
                                                    src={previewUrl}
                                                    alt="Preview"
                                                    className="w-full h-full object-cover"
                                                    onError={(e) => {
                                                        (e.target as HTMLImageElement).src =
                                                            'https://placehold.co/400?text=Invalid+Image';
                                                    }}
                                                />
                                            ) : (
                                                <p className={cn('px-4 text-center', Styles.colors.textMuted)}>
                                                    No image URL provided
                                                </p>
                                            )}
                                        </div>
                                    </div>
                                </CardContent>

                                <CardFooter className={cn('flex gap-4 p-8', Styles.backgrounds.footerDark)}>
                                    <Button
                                        type="button"
                                        variant="outline"
                                        className="flex-1 text-black bg-white border-white hover:bg-gray-200 transition-colors"
                                        onClick={goBack}
                                    >
                                        {MESSAGES.CANCEL_BUTTON}
                                    </Button>
                                    <Button
                                        type="submit"
                                        style={{ backgroundColor: Styles.colors.hubCyan }}
                                        className="flex-1 text-white font-bold shadow-lg shadow-blue-500/20 transition-all hover:opacity-90"
                                    >
                                        {MESSAGES.SUBMIT_BUTTON}
                                    </Button>
                                </CardFooter>
                            </form>
                        </Form>
                    </Card>
                </div>
            </div>
        </Fragment>
    );
}
