import { Fragment } from 'react/jsx-runtime';
import { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card.tsx';
import { Button } from '@/components/ui/button.tsx';
import { Helmet } from 'react-helmet';
import { SponsorFormFields } from '@/website/AdminPanelPage/DashboardPages/pages/SponsorsPage/components/SponsorshipFormFields.tsx';
import { SponsorsEditMessages, SponsorsAddMessages } from './messages.tsx';
import { Form } from '@/components/ui/form.tsx';
import {
    sponsorSchema,
    SponsorFormData,
    Sponsor,
} from '@/website/AdminPanelPage/DashboardPages/pages/SponsorsPage/validation/sponsor.tsx';
import { Styles } from '../../../AdminStyle.ts';
import { cn } from '@/lib/utils.ts';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/services/apiClient.ts';

export function SponsorsEditPage() {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const queryClient = useQueryClient();
    const isEditMode = Boolean(id);
    const MESSAGES = isEditMode ? SponsorsEditMessages : SponsorsAddMessages;

    const form = useForm<SponsorFormData>({
        resolver: zodResolver(sponsorSchema),
        defaultValues: {
            name: '',
            tier: '',
            logo_url: '',
            website_url: '',
        },
        mode: 'onTouched',
    });

    const { control, handleSubmit, reset, watch } = form;
    const logoUrl = watch('logo_url');

    // 1. Fetch data if in Edit Mode
    const { data: sponsor, isLoading } = useQuery({
        queryKey: ['sponsor', id],
        queryFn: () => apiClient.get<{ sponsor: Sponsor }>(`/admin/sponsors/${id}`),
        enabled: isEditMode, // Only run query if id exists
        select: (res) => res.sponsor,
    });
    // 2. Fill form when data is received
    useEffect(() => {
        if (sponsor) {
            reset({
                name: sponsor.name,
                tier: sponsor.tier,
                logo_url: sponsor.logo_url,
                website_url: sponsor.website_url,
            });
        }
    }, [sponsor, reset]);

    // 3. Mutation for Save (Create or Update)
    const mutation = useMutation({
        mutationFn: (formData: SponsorFormData) => {
            return isEditMode
                ? apiClient.patch<Sponsor, SponsorFormData>(`/admin/sponsors/${id}`, formData)
                : apiClient.post<Sponsor, SponsorFormData>(`/admin/sponsors`, formData);
        },
        onSuccess: async () => {
            await queryClient.invalidateQueries({ queryKey: ['sponsors'] });
            navigate('/admin/dashboard/sponsors');
        },
        onError: (error) => {
            alert(error.message);
        },
    });

    const onSubmit = (data: SponsorFormData) => {
        mutation.mutate(data);
    };

    const goBack = () => {
        navigate('/admin/dashboard/sponsors');
    };

    const pageWrapperClass = cn('min-h-screen p-8', Styles.backgrounds.primaryGradient);
    // Show loading state only when fetching existing data
    if (isEditMode && isLoading) {
        return (
            <div className={pageWrapperClass}>
                <div className="max-w-5xl mx-auto text-white text-center py-20">Loading sponsor details...</div>
            </div>
        );
    }

    if (isEditMode && !sponsor) {
        return (
            <Fragment>
                <Helmet>
                    <title>{SponsorsEditMessages.NOT_FOUND_TITLE}</title>
                </Helmet>
                <div className={pageWrapperClass}>
                    <div className="max-w-2xl mx-auto">
                        <Card className={cn('p-12 text-center', Styles.glass.card)}>
                            <p className="text-red-400 text-lg mb-6">{SponsorsEditMessages.NOT_FOUND_MESSAGE}</p>
                            <Button
                                style={{ backgroundColor: Styles.colors.hubCyan }}
                                className="text-white hover:opacity-90 transition-opacity"
                                onClick={goBack}
                            >
                                {SponsorsEditMessages.RETURN_BUTTON}
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
                                    <div className={Styles.forms.fieldContainer}>
                                        <div className="form-dark-theme">
                                            <SponsorFormFields control={control} />
                                        </div>
                                    </div>

                                    <div className="flex-1 flex flex-col items-center justify-start gap-4">
                                        <span className={cn('self-start !text-white', Styles.text.label)}>Preview</span>

                                        <div
                                            className={cn(
                                                'relative w-full max-w-[500px] aspect-square rounded-lg flex items-center justify-center overflow-hidden',
                                                Styles.backgrounds.previewBox,
                                            )}
                                        >
                                            {logoUrl ? (
                                                <img
                                                    src={logoUrl}
                                                    alt="Preview"
                                                    className="w-full h-full object-contain p-4"
                                                    onError={(e) => {
                                                        (e.target as HTMLImageElement).src =
                                                            'https://placehold.co/300?text=Invalid+Image';
                                                    }}
                                                />
                                            ) : (
                                                <p className={cn('px-4 text-center', Styles.colors.textMuted)}>
                                                    No logo URL provided
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
