import { Fragment, useState } from 'react';
import { Link } from 'react-router';
import { Helmet } from 'react-helmet';

import FeatureSwitchCard from '@/website/AdminPanelPage/DashboardPages/pages/FeatureSwitchesPage/components/FeatureSwitchCard.tsx';
import { Card } from '@/components/ui/card.tsx';
import { Button } from '@/components/ui/button.tsx';

import { FeatureSwitchesMessages as MESSAGES } from './messages.tsx';
import { Styles } from '../../../AdminStyle.ts';
import { cn } from '@/lib/utils.ts';

import { getAllFeatureSwitches, toggleFeatureSwitch } from './store/useFeatureSwitches.ts';
import type { FeatureSwitch } from './types.ts';

export default function FeatureSwitchesPage() {
    const [items, setItems] = useState<FeatureSwitch[]>(() => getAllFeatureSwitches());

    function refresh() {
        setItems(getAllFeatureSwitches());
    }

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

                    {items.length === 0 ? (
                        <Card className={cn('p-20 text-center border-dashed', Styles.glass.card)}>
                            <p className={cn('text-xl font-medium', Styles.text.subtitle)}>{MESSAGES.EMPTY_STATE}</p>
                        </Card>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                            {items.map((it) => (
                                <div key={it.id} className="group">
                                    <FeatureSwitchCard
                                        name={it.name}
                                        currentState={it.currentState}
                                        onToggle={() => {
                                            toggleFeatureSwitch(it.id);
                                            refresh();
                                        }}
                                        toggleOnLabel={MESSAGES.TOGGLE_ON}
                                        toggleOffLabel={MESSAGES.TOGGLE_OFF}
                                        statusOnLabel={MESSAGES.STATUS_ON}
                                        statusOffLabel={MESSAGES.STATUS_OFF}
                                        className={cn(
                                            'transition-all duration-300 group-hover:translate-y-[-4px]',
                                            Styles.glass.card,
                                            Styles.glass.cardHover,
                                            'rounded-2xl',
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
