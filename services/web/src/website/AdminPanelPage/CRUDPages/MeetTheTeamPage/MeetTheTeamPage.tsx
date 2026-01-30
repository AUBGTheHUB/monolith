import { Fragment, useState } from 'react';
import { Link } from 'react-router';
import { AdminCard } from '@/internalLibrary/AdminCard/adminCard.tsx';
import { Card } from '@/components/ui/card.tsx';
import { Button } from '@/components/ui/button.tsx';
import { Helmet } from 'react-helmet';
import { TeamPageMessages as MESSAGES } from './messages.tsx';
import { Styles } from '../../AdminStyle.ts';
import { cn } from '@/lib/utils.ts';
import teamMembersData from './resources/teamMembers.json';

import { TeamMemberFormData } from './validation/validation.tsx';

interface TeamMember extends TeamMemberFormData {
    id: string;
}

export function MeetTheTeamPage() {
    const [members, setMembers] = useState<TeamMember[]>(teamMembersData as unknown as TeamMember[]);

    const handleDelete = (id: string, name: string) => {
        if (window.confirm(MESSAGES.DELETE_CONFIRM(name))) {
            setMembers((prev) => prev.filter((m) => m.id !== id));
        }
    };

    const renderMemberActions = (id: string, name: string) => (
        <div className="flex gap-3 w-full">
            <Link to={`/admin/meet-the-team/${id}`} className="flex-1">
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
                onClick={() => handleDelete(id, name)}
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

                        <Link to="/admin/meet-the-team/add">
                            <Button
                                size="lg"
                                style={{ backgroundColor: Styles.colors.hubCyan }}
                                className={cn('px-8 py-6 text-lg', Styles.actions.primaryButton)}
                            >
                                {MESSAGES.ADD_BUTTON}
                            </Button>
                        </Link>
                    </div>

                    {members.length === 0 ? (
                        <Card className={cn('p-20 text-center border-dashed', Styles.glass.card)}>
                            <p className={cn('text-xl font-medium', Styles.text.subtitle)}>{MESSAGES.EMPTY_STATE}</p>
                        </Card>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                            {members.map((member) => (
                                <div key={member.id} className="group">
                                    <AdminCard
                                        imageUrl={member.image || ''}
                                        imageAlt={member.name}
                                        title={member.name}
                                        subtitle={member.departments.join(', ')} // Display departments as subtitle
                                        actions={renderMemberActions(member.id, member.name)}
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
