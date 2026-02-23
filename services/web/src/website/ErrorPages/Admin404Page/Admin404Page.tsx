import { Link } from 'react-router';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Helmet } from 'react-helmet';
import { Styles } from '../../AdminPanelPage/AdminStyle';
import { cn } from '@/lib/utils';

export function Admin404Page() {
    return (
        <>
            <Helmet>
                <title>404 - Not Found | Admin Panel</title>
            </Helmet>
            <div
                className={cn(
                    'min-h-screen p-8 flex flex-col items-center justify-center',
                    Styles.backgrounds.primaryGradient,
                )}
            >
                <div className="max-w-md w-full mx-auto text-center">
                    <h1 className={cn('text-5xl mb-12', Styles.text.title)}>
                        Admin <span style={{ color: Styles.colors.hubCyan }}>Panel</span>
                    </h1>

                    <Card className={cn('flex flex-col transition-all duration-500', Styles.glass.card)}>
                        <CardHeader className="pt-10">
                            <div className="text-8xl font-bold mb-4" style={{ color: Styles.colors.hubCyan }}>
                                404
                            </div>
                            <CardTitle className={cn('text-3xl opacity-90', Styles.text.title)}>
                                Page Not Found
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="pb-10 px-10 space-y-6">
                            <p className={cn(Styles.text.subtitle, 'text-lg')}>
                                Searched Address Not Found. It seems like Hubzie took a wrong turn!
                            </p>

                            <Link to="/admin/dashboard" className="block">
                                <Button
                                    className={cn('w-full h-14 text-lg border-0', Styles.actions.primaryButton)}
                                    style={{ backgroundColor: Styles.colors.hubCyan }}
                                >
                                    Back to Dashboard
                                </Button>
                            </Link>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </>
    );
}
