<<<<<<< HEAD
import { Fragment, useState } from 'react';
import { Link } from 'react-router';
import { MOCK_SPONSORS, Sponsor } from './mockSponsors';
import { AdminCard } from '@/internalLibrary/AdminCard/adminCard';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Helmet } from 'react-helmet';
import { SponsorsPageMessages as MESSAGES } from './messages';
import { Styles } from '../../../AdminStyle';
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
            <Link to={`/admin/dashboard/sponsors/${sponsorId}`} className="flex-1">
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

                        <Link to="/admin/dashboard/sponsors/add">
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
=======
import { Card, CardFooter, CardContent } from '@/components/ui/card';
import sponsors from './sponsors.json';
import { Button } from '@/components/ui/button';
import { Plus } from 'lucide-react';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router';

export default function SponsorsPage() {
    const navigate = useNavigate();

    const [localSponsors, setLocalSponsors] = useState<typeof sponsors>([]);

    useEffect(() => {
        try {
            const stored = localStorage.getItem('sponsors');
            if (stored) {
                setLocalSponsors(JSON.parse(stored));
            } else {
                localStorage.setItem('sponsors', JSON.stringify(sponsors));
                setLocalSponsors(sponsors);
            }
        } catch {
            setLocalSponsors(sponsors);
        }
    }, []);

    const handleDelete = (id: number) => {
        const updated = localSponsors.filter((s) => s.id !== id);
        setLocalSponsors(updated);
        localStorage.setItem('sponsors', JSON.stringify(updated));
    };

    return (
        <div className="p-8 relative min-h-screen bg-gray-50 text-gray-900">
            <div className="max-w-7xl mx-auto">
                <h1 className="text-3xl font-bold mb-6 text-gray-900">Sponsors</h1>

                <div className="flex flex-wrap -mx-2 gap-6">
                    {localSponsors.map((sponsor) => (
                        <Card
                            key={sponsor.id}
                            className="flex flex-col items-center justify-between rounded-2xl shadow-sm hover:shadow-md transition-all p-4 bg-white text-black w-80 mx-2"
                        >
                            <CardContent className="flex flex-col items-center gap-2 w-full">
                                <div className="w-full h-40 relative rounded-xl overflow-hidden bg-gray-100">
                                    <img
                                        src={sponsor.image}
                                        alt={sponsor.name}
                                        className="object-contain p-2 w-full h-full"
                                    />
                                </div>
                                <div className="text-center font-semibold mt-2 text-gray-900">{sponsor.name}</div>
                            </CardContent>
                            <CardFooter className="flex justify-between w-full gap-2">
                                <Button
                                    variant="destructive"
                                    className="w-1/2 bg-black text-white hover:opacity-90"
                                    onClick={() => handleDelete(sponsor.id)}
                                >
                                    Delete
                                </Button>
                                <Button
                                    variant="secondary"
                                    className="w-1/2 bg-blue-600 text-white hover:bg-blue-700"
                                    onClick={() => navigate(`/dashboard/sponsors/edit/${sponsor.id}`)}
                                >
                                    Edit
                                </Button>
                            </CardFooter>
                        </Card>
                    ))}
                </div>

                <Button
                    className="fixed bottom-8 right-8 rounded-full h-14 w-14 shadow-lg bg-blue-600 text-white hover:bg-blue-700"
                    size="icon"
                    onClick={() => navigate('/dashboard/sponsors/add')}
                >
                    <Plus className="h-6 w-6" />
                </Button>
            </div>
        </div>
>>>>>>> 9ced9e8 (Added Sponsorship Pages (#1086))
    );
}
