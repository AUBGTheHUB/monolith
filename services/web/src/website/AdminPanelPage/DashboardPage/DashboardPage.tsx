import { Fragment } from 'react/jsx-runtime';
import { Link } from 'react-router';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Helmet } from 'react-helmet';

export function DashboardPage() {
    return (
        <Fragment>
            <Helmet>
                <title>Admin Panel - The Hub AUBG</title>
                <link rel="icon" href="/faviconHack.ico" />
            </Helmet>
            <div className="min-h-screen bg-gray-50 p-8">
                <div className="max-w-7xl mx-auto">
                    <h1 className="text-4xl font-bold mb-8 text-center">Admin Panel of The Huqb</h1>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {/* Judges Container */}
                        <Card className="h-64 flex flex-col">
                            <CardHeader className="flex-grow flex items-center justify-center">
                                <CardTitle className="text-3xl">Judges</CardTitle>
                            </CardHeader>
                            <CardContent className="pb-6">
                                <Link to="/dashboard/judges">
                                    <Button className="w-full h-14 text-lg bg-blue-600 hover:bg-blue-700">View</Button>
                                </Link>
                            </CardContent>
                        </Card>

                        <Card className="h-64 flex flex-col">
                            <CardHeader className="flex-grow flex items-center justify-center">
                                <CardTitle className="text-3xl">Judges</CardTitle>
                            </CardHeader>
                            <CardContent className="pb-6">
                                <Link to="/dashboard/judges">
                                    <Button className="w-full h-14 text-lg bg-blue-600 hover:bg-blue-700">View</Button>
                                </Link>
                            </CardContent>
                        </Card>

                        {/* Placeholder for future admin features - uncomment when ready */}
                        {/* 
                        <Card className="h-64 flex flex-col">
                            <CardHeader className="flex-grow flex items-center justify-center">
                                <CardTitle className="text-3xl">Feature Name</CardTitle>
                            </CardHeader>
                            <CardContent className="pb-6">
                                <Link to="/dashboard/feature-switches">
                                    <Button className="w-full h-14 text-lg bg-blue-600 hover:bg-blue-700">
                                        View
                                    </Button>
                                </Link>
                            </CardContent>
                        </Card>
                        */}
                    </div>
                </div>
            </div>
        </Fragment>
    );
}
