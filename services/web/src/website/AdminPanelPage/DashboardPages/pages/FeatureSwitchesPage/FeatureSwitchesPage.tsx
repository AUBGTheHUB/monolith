import { Fragment } from 'react';
import { Link } from 'react-router';
import { Helmet } from 'react-helmet';

import FeatureSwitchCard from '@/website/AdminPanelPage/DashboardPages/pages/FeatureSwitchesPage/components/FeatureSwitchCard.tsx';
import { Card } from '@/components/ui/card.tsx';
import { Button } from '@/components/ui/button.tsx';

import { FeatureSwitchesMessages as MESSAGES } from './messages.tsx';
import { Styles } from '../../../AdminStyle.ts';
import { cn } from '@/lib/utils.ts';

import type { FeatureSwitch, FeatureSwitchFormData } from './types.ts';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/services/apiClient.ts';

export default function FeatureSwitchesPage() {
    const queryClient = useQueryClient();

    // 1. Fetch switches
    const { data: features, isLoading } = useQuery({
        queryKey: ['feature-switches'],
        queryFn: () => apiClient.get<{ features: FeatureSwitch[] }>(`/feature-switches`),
        select: (res) => res.features,
    });

    // 3. Mutation for Toggle
    const mutation = useMutation({
        mutationFn: (formData: FeatureSwitchFormData) => {
            return apiClient.patch<FeatureSwitch, FeatureSwitchFormData>('/feature-switches', formData);
        },
        onSuccess: async () => {
            await queryClient.invalidateQueries({ queryKey: ['feature-switches'] });
        },
        onError: (error) => {
            alert(error.message);
        },
    });
    const handleToggle = (fs: FeatureSwitch) => {
        mutation.mutate({
            name: fs.name,
            state: !fs.state,
        });
    };
    return (
        <Fragment>
            <Helmet>
                <title>{MESSAGES.PAGE_TITLE}</title>
            </Helmet>

            <div className={cn('min-h-screen p-8', Styles.backgrounds.primaryGradient)}>
                <div className="max-w-7xl mx-auto">
                    <Link to="/admin/dashboard">
                        <Button variant="ghost" className={cn('mb-6', Styles.glass.ghostButton)}>
                            {MESSAGES.BACK_BUTTON}
                        </Button>
                    </Link>

                    <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-12">
                        <div>
                            <h1 className={cn('text-4xl', Styles.text.title)}>{MESSAGES.HEADING}</h1>
                            <p className={Styles.text.subtitle}>{MESSAGES.SUBTITLE}</p>
                        </div>
                    </div>

                    {isLoading ? (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                            {[1, 2, 3].map((i) => (
                                <Card key={i} className={cn('h-48 animate-pulse', Styles.glass.card)} />
                            ))}
                        </div>
                    ) : features?.length === 0 ? (
                        <Card className={cn('p-20 text-center border-dashed', Styles.glass.card)}>
                            <p className={cn('text-xl font-medium', Styles.text.subtitle)}>{MESSAGES.EMPTY_STATE}</p>
                        </Card>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                            {features?.map((fs) => (
                                <div key={fs.id} className="group">
                                    <FeatureSwitchCard
                                        name={fs.name}
                                        currentState={fs.state}
                                        onToggle={() => handleToggle(fs)}
                                        toggleOnLabel={MESSAGES.TOGGLE_ON}
                                        toggleOffLabel={MESSAGES.TOGGLE_OFF}
                                        statusOnLabel={MESSAGES.STATUS_ON}
                                        statusOffLabel={MESSAGES.STATUS_OFF}
                                        className={cn(
                                            'transition-all duration-300 group-hover:translate-y-[-4px]',
                                            Styles.glass.card,
                                            Styles.glass.cardHover,
                                            'rounded-2xl',
                                            mutation.isPending && 'opacity-70 pointer-events-none',
                                        )}
                                    />
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </Fragment>
    );
}
