import { Fragment, useState } from 'react';
import { Link } from 'react-router';
import { MOCK_SPONSORS, Sponsor } from './mockSponsors';
import { AdminCard } from '@/internalLibrary/AdminCard/adminCard';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Helmet } from 'react-helmet';
import { SponsorsPageMessages as MESSAGES } from './messages';
import { Styles } from '../../../AdminStyles';
import { cn } from '@/lib/utils';

export function SponsorsListPage() {
    const [sponsors, setSponsors] = useState<Sponsor[]>(MOCK_SPONSORS);

    const getTierColors = (tier: string): { text: string; bg: string } => {
        const tierLower = tier.toLowerCase().trim();

        const tierColorMap: Record<string, { text: string; bg: string }> = {
            gold: { text: 'text-amber-900', bg: 'bg-gradient-to-r from-amber-400 to-yellow-300' },
            silver: { text: 'text-slate-100', bg: 'bg-gradient-to-r from-slate-400 to-slate-300' },
            bronze: { text: 'text-orange-950', bg: 'bg-gradient-to-r from-orange-600 to-orange-400' },
            platinum: { text: 'text-cyan-900', bg: 'bg-gradient-to-r from-cyan-300 to-blue-200' },
            diamond: { text: 'text-blue-900', bg: 'bg-gradient-to-r from-blue-400 to-purple-400' },
            partner: { text: 'text-emerald-100', bg: 'bg-gradient-to-r from-emerald-500 to-teal-400' },
            sponsor: { text: 'text-pink-100', bg: 'bg-gradient-to-r from-pink-500 to-rose-400' },
        };

        return tierColorMap[tierLower] || { text: 'text-white', bg: 'bg-gradient-to-r from-blue-500 to-purple-500' };
    };

    const handleDelete = (id: string) => {
        const sponsor = sponsors.find((s) => s.id === id);
        if (!sponsor) return;

        if (window.confirm(MESSAGES.DELETE_CONFIRM(sponsor.name))) {
            setSponsors((prevSponsors) => prevSponsors.filter((s) => s.id !== id));
        }
    };

    const renderSponsorActions = (sponsorId: string) => (
        <div className="flex gap-3 w-full">
            <Link to={`admin/sponsors/${sponsorId}`} className="flex-1">
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
                onClick={() => handleDelete(sponsorId)}
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

                        <Link to="/admin/sponsors/add">
                            <Button
                                size="lg"
                                style={{ backgroundColor: Styles.colors.hubCyan }}
                                className={cn('px-8 py-6 text-lg', Styles.actions.primaryButton)}
                            >
                                {MESSAGES.ADD_BUTTON}
                            </Button>
                        </Link>
                    </div>

                    {sponsors.length === 0 ? (
                        <Card className={cn('p-20 text-center border-dashed', Styles.glass.card)}>
                            <p className={cn('text-xl font-medium', Styles.text.subtitle)}>{MESSAGES.EMPTY_STATE}</p>
                        </Card>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                            {sponsors.map((sponsor) => {
                                const tierColors = getTierColors(sponsor.tier);
                                return (
                                    <div key={sponsor.id} className="group">
                                        <AdminCard
                                            imageUrl={sponsor.logoUrl}
                                            imageAlt={sponsor.name}
                                            title={sponsor.name}
                                            subtitle={sponsor.tier}
                                            tierColor={tierColors.text}
                                            tierBgColor={tierColors.bg}
                                            position={sponsor.careersUrl ? 'Careers Available' : ''}
                                            linkedinUrl={sponsor.websiteUrl}
                                            actions={renderSponsorActions(sponsor.id)}
                                            className={cn(
                                                'transition-all duration-300 group-hover:translate-y-[-4px]',
                                                Styles.glass.card,
                                                Styles.glass.cardHover,
                                                'rounded-2xl',
                                            )}
                                        />
                                    </div>
                                );
                            })}
                        </div>
                    )}
                </div>
            </div>
        </Fragment>
    );
}
