import { Fragment } from 'react/jsx-runtime';
import { useState } from 'react';
import { Link } from 'react-router';
import { MOCK_JUDGES, Judge } from '../../../lib/judges.mock';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Helmet } from 'react-helmet';

export function JudgesListPage() {
    const [judges, setJudges] = useState<Judge[]>(MOCK_JUDGES);

    const handleDelete = (id: string) => {
        if (window.confirm('Are you sure you want to delete this judge?')) {
            setJudges(judges.filter((judge) => judge.id !== id));
        }
    };

    return (
        <Fragment>
            <Helmet>
                <title>Judges - Admin Dashboard</title>
                <link rel="icon" href="/faviconHack.ico" />
            </Helmet>
            <div className="min-h-screen bg-gray-50 p-8">
                <div className="max-w-7xl mx-auto">
                    {/* Back to Dashboard Button */}
                    <Link to="/dashboard">
                        <Button variant="ghost" className="mb-4">
                            ← Back to Dashboard
                        </Button>
                    </Link>

                    <div className="flex justify-between items-center mb-8">
                        <div>
                            <h1 className="text-4xl font-bold">Judges</h1>
                            <p className="text-gray-600 mt-2">Manage hackathon judges</p>
                        </div>
                        <Link to="/dashboard/judges/add">
                            <Button size="lg" className="bg-blue-600 hover:bg-blue-700">
                                + Add New Judge
                            </Button>
                        </Link>
                    </div>

                    {judges.length === 0 ? (
                        <Card className="p-12 text-center">
                            <p className="text-gray-500 text-lg">
                                No judges added yet. Click &quot;Add New Judge&quot; to get started.
                            </p>
                        </Card>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {judges.map((judge) => (
                                <Card key={judge.id} className="overflow-hidden hover:shadow-lg transition-shadow">
                                    <CardHeader className="bg-gradient-to-br from-blue-50 to-white p-6">
                                        <div className="flex flex-col items-center">
                                            <img
                                                src={judge.imageUrl}
                                                alt={judge.name}
                                                className="w-32 h-32 rounded-full object-cover border-4 border-white shadow-lg mb-4"
                                            />
                                            <CardTitle className="text-xl text-center">{judge.name}</CardTitle>
                                            <p className="text-sm text-gray-600 text-center mt-1">
                                                {judge.companyName}
                                            </p>
                                        </div>
                                    </CardHeader>
                                    <CardContent className="p-4 flex gap-2">
                                        <Link to={`/dashboard/judges/${judge.id}`} className="flex-1">
                                            <Button variant="outline" className="w-full">
                                                Edit
                                            </Button>
                                        </Link>
                                        <Button
                                            variant="destructive"
                                            className="flex-1"
                                            onClick={() => handleDelete(judge.id)}
                                        >
                                            Delete
                                        </Button>
                                    </CardContent>
                                </Card>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </Fragment>
    );
}
