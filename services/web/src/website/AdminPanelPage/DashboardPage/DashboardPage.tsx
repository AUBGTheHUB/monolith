import { Fragment } from 'react/jsx-runtime';
import { Link } from 'react-router';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Helmet } from 'react-helmet';
import { Styles } from '../AdminStyles';
import { cn } from '@/lib/utils';

export function DashboardPage() {
    return (
        <Fragment>
            <Helmet>
                <title>Admin Panel - The Hub AUBG</title>
            </Helmet>
            <div
                className={cn(
                    'min-h-screen p-8 flex flex-col items-center justify-center',
                    Styles.backgrounds.primaryGradient,
                )}
            >
                <div className="max-w-7xl w-full mx-auto">
                    <h1 className={cn('text-5xl mb-16 text-center', Styles.text.title)}>
                        Admin <span style={{ color: Styles.colors.hubCyan }}>Panel</span>
                    </h1>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        {/* Judges Container */}
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
                                    Judges
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="pb-10 px-10">
                                <Link to="/dashboard/judges">
                                    <Button
                                        className={cn('w-full h-14 text-lg border-0', Styles.actions.primaryButton)}
                                        style={{ backgroundColor: Styles.colors.hubCyan }}
                                    >
                                        View
                                    </Button>
                                </Link>
                            </CardContent>
                        </Card>

                        {/* feature-switches Container */}
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
                                    Feature Switches
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="pb-10 px-10">
                                <Link to="/dashboard/feature-switches">
                                    <Button
                                        className={cn('w-full h-14 text-lg border-0', Styles.actions.primaryButton)}
                                        style={{ backgroundColor: Styles.colors.hubCyan }}
                                    >
                                        View
                                    </Button>
                                </Link>
                            </CardContent>
                        </Card>

                        {/* Sponsors Container */}
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
                                    Sponsors
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="pb-10 px-10">
                                <Link to="/dashboard/sponsors">
                                    <Button
                                        className={cn('w-full h-14 text-lg border-0', Styles.actions.primaryButton)}
                                        style={{ backgroundColor: Styles.colors.hubCyan }}
                                    >
                                        View
                                    </Button>
                                </Link>
                            </CardContent>
                        </Card>

                        {/* Meet The Team Container */}
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
                                    Meet The Team
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="pb-10 px-10">
                                <Link to="/dashboard/meet-the-team">
                                    <Button
                                        className={cn('w-full h-14 text-lg border-0', Styles.actions.primaryButton)}
                                        style={{ backgroundColor: Styles.colors.hubCyan }}
                                    >
                                        View
                                    </Button>
                                </Link>
                            </CardContent>
                        </Card>

                        {/*Mentors Container */}
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
                                    Mentors
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="pb-10 px-10">
                                <Link to="/dashboard/mentors">
                                    <Button
                                        className={cn('w-full h-14 text-lg border-0', Styles.actions.primaryButton)}
                                        style={{ backgroundColor: Styles.colors.hubCyan }}
                                    >
                                        View
                                    </Button>
                                </Link>
                            </CardContent>
                        </Card>

                        {/* Past Events Container */}
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
                                    Past Events
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="pb-10 px-10">
                                <Link to="/dashboard/past-events">
                                    <Button
                                        className={cn('w-full h-14 text-lg border-0', Styles.actions.primaryButton)}
                                        style={{ backgroundColor: Styles.colors.hubCyan }}
                                    >
                                        View
                                    </Button>
                                </Link>
                            </CardContent>
                        </Card>

                        {/* AWS Access page Container */}
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
                                        'text-3xl text-center opacity-90 transition-colors group-hover:text-white',
                                        Styles.text.title,
                                    )}
                                >
                                    AWS Access - S3 Bucket
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="pb-10 px-10">
                                <Link to="/dashboard/s3-bucket">
                                    <Button
                                        className={cn('w-full h-14 text-lg border-0', Styles.actions.primaryButton)}
                                        style={{ backgroundColor: Styles.colors.hubCyan }}
                                    >
                                        View
                                    </Button>
                                </Link>
                            </CardContent>
                        </Card>
                    </div>
                </div>
            </div>
        </Fragment>
    );
}
