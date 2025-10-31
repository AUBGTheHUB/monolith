import { Fragment } from 'react/jsx-runtime';
import { useState } from 'react';
import { Link } from 'react-router';
import { MOCK_JUDGES, Judge } from '@/lib/judges.mock';
import { AdminCard } from '@/components/ui/admin-card';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Helmet } from 'react-helmet';

// Text constants so it is easier to navigate and manage. Also better readability.
const MESSAGES = {
    PAGE_TITLE: 'Judges - Admin Dashboard',
    HEADING: 'Judges',
    SUBTITLE: 'Manage hackathon judges',
    BACK_BUTTON: '← Back to Dashboard',
    ADD_BUTTON: '+ Add New Judge',
    EMPTY_STATE: 'No judges added yet. Click "Add New Judge" to get started.',
    DELETE_CONFIRM: (name: string) => `Are you sure you want to delete ${name}?`,
    EDIT_BUTTON: 'Edit',
    DELETE_BUTTON: 'Delete',
};

export function JudgesListPage() {
    // State: List of all judges (initialized with mock data which can be found in lib/judges.mock.ts)
    const [judges, setJudges] = useState<Judge[]>(MOCK_JUDGES);

    /**
     * DELETE a judge 
     * @param id - The unique identifier of the judge to delete
     */
    const handleDelete = (id: string) => {
        // Find the judge by ID to show their name in confirmation
        const judge = judges.find((j) => j.id === id);

        // If judge doesn't exist, exit early
        if (!judge) {
            console.error(`Judge with id ${id} not found`);
            return;
        }

        // Ask for confirmation with judge's name for better UX : )
        if (window.confirm(MESSAGES.DELETE_CONFIRM(judge.name))) {
            // Remove the judge from the list using filter
            setJudges((prevJudges) => prevJudges.filter((j) => j.id !== id));
        }
    };

    /**
     * Renders the action buttons (Edit and Delete) for each judge card
     * @param judgeId - The ID of the judge for routing and deletion
     * @returns JSX with Edit and Delete buttons
     */
    const renderJudgeActions = (judgeId: string) => (
        <>
            {/* Edit Button - Links to the edit page */}
            <Link to={`/dashboard/judges/${judgeId}`} className="flex-1">
                <Button variant="outline" className="w-full">
                    {MESSAGES.EDIT_BUTTON}
                </Button>
            </Link>

            {/* Delete Button - Triggers delete confirmation */}
            <Button variant="destructive" className="flex-1" onClick={() => handleDelete(judgeId)}>
                {MESSAGES.DELETE_BUTTON}
            </Button>
        </>
    );

    return (
        <Fragment>
            {/* SEO: Sets the page title in the browser tab, very cool!*/}
            <Helmet>
                <title>{MESSAGES.PAGE_TITLE}</title>
            </Helmet>

            {/* Main Container: Full height with gray background */}
            <div className="min-h-screen bg-gray-50 p-8">
                <div className="max-w-7xl mx-auto">
                    {/* Back Navigation Button */}
                    <Link to="/dashboard">
                        <Button variant="ghost" className="mb-4">
                            {MESSAGES.BACK_BUTTON}
                        </Button>
                    </Link>

                    {/* Page Header: Title, subtitle, and Add button */}
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

                    {/* Conditional Rendering: Show empty state OR judge cards */}
                    {judges.length === 0 ? (
                        // Empty State: Shown when no judges exist
                        <Card className="p-12 text-center">
                            <p className="text-gray-500 text-lg">{MESSAGES.EMPTY_STATE}</p>
                        </Card>
                    ) : (
                        // Judges Grid: Responsive layout (1/2/3 columns based on screen size)
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
