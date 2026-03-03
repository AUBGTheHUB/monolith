import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.tsx';
import { cn } from '@/lib/utils.ts';
import { Styles } from '@/website/AdminPanelPage/AdminStyle.ts';
import { Link, To } from 'react-router';

type AdminPageCardProps = {
    title: string;
    link: To;
};

export default function AdminPageCard({ title, link }: AdminPageCardProps) {
    return (
        <Card
            className={cn(
                'h-72 flex flex-col group transition-all duration-500',
                Styles.glass.card,
                Styles.glass.cardHover,
            )}
        >
            <CardHeader className="flex-grow flex items-center justify-center pt-10">
                <CardTitle
                    className={cn(
                        'text-4xl text-center opacity-90 transition-colors group-hover:text-white',
                        Styles.text.title,
                    )}
                >
                    {title}
                </CardTitle>
            </CardHeader>
            <CardContent className="pb-10 px-10">
                <Link to={link}>
                    <Button
                        className={cn('w-full h-14 text-lg border-0', Styles.actions.primaryButton)}
                        style={{ backgroundColor: Styles.colors.hubCyan }}
                    >
                        View
                    </Button>
                </Link>
            </CardContent>
        </Card>
    );
}
