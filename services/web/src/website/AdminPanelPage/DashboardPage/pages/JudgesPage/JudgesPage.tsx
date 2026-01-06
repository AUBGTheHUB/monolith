import { Fragment } from 'react/jsx-runtime';
import { useState } from 'react';
import { Link } from 'react-router';
import { MOCK_JUDGES } from '@/lib/judges.mock';
import { Judge } from '@/lib/types';
import { AdminCard } from '@/components/ui/admin-card';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Helmet } from 'react-helmet';
import { JudgesPageMessages as MESSAGES } from './messagesConsts';

export function JudgesListPage() {
    const [judges, setJudges] = useState<Judge[]>(MOCK_JUDGES);

    const handleDelete = (id: string) => {
        const judge = judges.find((j) => j.id === id);

        if (!judge) {
            console.error(`Judge with id ${id} not found`);
            return;
        }

        if (window.confirm(MESSAGES.DELETE_CONFIRM(judge.name))) {
            setJudges((prevJudges) => prevJudges.filter((j) => j.id !== id));
        }
    };

    const renderJudgeActions = (judgeId: string) => (
        <>
            <Link to={`/dashboard/judges/${judgeId}`} className="flex-1">
                <Button variant="outline" className="w-full">
                    {MESSAGES.EDIT_BUTTON}
                </Button>
            </Link>

            <Button variant="destructive" className="flex-1" onClick={() => handleDelete(judgeId)}>
                {MESSAGES.DELETE_BUTTON}
            </Button>
        </>
    );

    return (
        <Fragment>
            <Helmet>
                <title>{MESSAGES.PAGE_TITLE}</title>
            </Helmet>

            <div className="min-h-screen bg-gray-50 p-8">
                <div className="max-w-7xl mx-auto">
                    <Link to="/dashboard">
                        <Button variant="ghost" className="mb-4">
                            {MESSAGES.BACK_BUTTON}
                        </Button>
                    </Link>

                    <div className="flex justify-between items-center mb-8">
                        <div>
                            <h1 className="text-4xl font-bold">{MESSAGES.HEADING}</h1>
                            <p className="text-gray-600 mt-2">{MESSAGES.SUBTITLE}</p>
                        </div>
                        <Link to="/dashboard/judges/add">
                            <Button size="lg" className="bg-blue-600 hover:bg-blue-700">
                                {MESSAGES.ADD_BUTTON}
                            </Button>
                        </Link>
                    </div>

                    {judges.length === 0 ? (
                        <Card className="p-12 text-center">
                            <p className="text-gray-500 text-lg">{MESSAGES.EMPTY_STATE}</p>
                        </Card>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {judges.map((judge) => (
                                <AdminCard
                                    key={judge.id}
                                    imageUrl={judge.imageUrl}
                                    imageAlt={judge.name}
                                    title={judge.name}
                                    subtitle={judge.companyName}
                                    actions={renderJudgeActions(judge.id)}
                                />
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </Fragment>
    );
}
