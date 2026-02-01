import { Fragment, useState } from 'react';
import { Link } from 'react-router';
import { MOCK_JUDGES } from '@/website/AdminPanelPage/DashboardPages/pages/JudgesPage/mockJudges.ts';
import { Judge } from '@/types/judge.ts';
import { AdminCard } from '@/internalLibrary/AdminCard/adminCard.tsx';
import { Card } from '@/components/ui/card.tsx';
import { Button } from '@/components/ui/button.tsx';
import { Helmet } from 'react-helmet';
import { JudgesPageMessages as MESSAGES } from './messages.tsx';
import { Styles } from '../../../AdminStyle.ts';
import { cn } from '@/lib/utils.ts';

export function JudgesListPage() {
    const [judges, setJudges] = useState<Judge[]>(MOCK_JUDGES);

    const handleDelete = (id: string) => {
        const judge = judges.find((j) => j.id === id);
        if (!judge) return;

        if (window.confirm(MESSAGES.DELETE_CONFIRM(judge.name))) {
            setJudges((prevJudges) => prevJudges.filter((j) => j.id !== id));
        }
    };

    const renderJudgeActions = (judgeId: string) => (
        <div className="flex gap-3 w-full">
            <Link to={`/admin/dashboard/judges/${judgeId}`} className="flex-1">
                <Button
                    variant="outline"
                    className="w-full bg-white/5 border-white/10 text-white hover:bg-white/20 hover:text-white transition-all"
                >
                    {MESSAGES.EDIT_BUTTON}
                </Button>
            </Link>

            <Button
                variant="destructive"
                className="flex-1 shadow-lg shadow-red-500/10 hover:shadow-red-500/20 transition-all"
                onClick={() => handleDelete(judgeId)}
            >
                {MESSAGES.DELETE_BUTTON}
            </Button>
        </div>
    );

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

                        <Link to="/admin/dashboard/judges/add">
                            <Button
                                size="lg"
                                style={{ backgroundColor: Styles.colors.hubCyan }}
                                className={cn('px-8 py-6 text-lg', Styles.actions.primaryButton)}
                            >
                                {MESSAGES.ADD_BUTTON}
                            </Button>
                        </Link>
                    </div>

                    {judges.length === 0 ? (
                        <Card className={cn('p-20 text-center border-dashed', Styles.glass.card)}>
                            <p className={cn('text-xl font-medium', Styles.text.subtitle)}>{MESSAGES.EMPTY_STATE}</p>
                        </Card>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                            {judges.map((judge) => (
                                <div key={judge.id} className="group">
                                    <AdminCard
                                        imageUrl={judge.imageUrl}
                                        imageAlt={judge.name}
                                        title={judge.name}
                                        subtitle={judge.companyName}
                                        position={judge.position}
                                        linkedinUrl={judge.linkedinURL}
                                        actions={renderJudgeActions(judge.id)}
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
