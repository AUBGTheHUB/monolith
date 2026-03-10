import { Fragment, useEffect } from 'react';
import { Link } from 'react-router';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Helmet } from 'react-helmet';
import { Styles } from '../../../AdminStyle';
import { cn } from '@/lib/utils';
import { apiClient } from '@/services/apiClient';
import { useQuery } from '@tanstack/react-query';
import type { Participant } from '@/types/participant';
import { columns } from './columns';
import { DataTable } from './data-table';

const BACK_BUTTON = (
    <span className="flex items-center gap-1">
        <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="currentColor"
            className="icon icon-tabler icons-tabler-filled icon-tabler-caret-left"
        >
            <path stroke="none" d="M0 0h24v24H0z" fill="none" />
            <path d="M13.883 5.007l.058 -.005h.118l.058 .005l.06 .009l.052 .01l.108 .032l.067 .027l.132 .07l.09 .065l.081 .073l.083 .094l.054 .077l.054 .096l.017 .036l.027 .067l.032 .108l.01 .053l.01 .06l.004 .057l.002 .059v12c0 .852 -.986 1.297 -1.623 .783l-.084 -.076l-6 -6a1 1 0 0 1 -.083 -1.32l.083 -.094l6 -6l.094 -.083l.077 -.054l.096 -.054l.036 -.017l.067 -.027l.108 -.032l.053 -.01l.06 -.01z" />
        </svg>
        Back to Dashboard
    </span>
);

export function ParticipantsPage() {
    const { data, isLoading, error, isError } = useQuery({
        queryKey: ['participants'],
        queryFn: () => apiClient.get<{ participants: Participant[] }>('/hackathon/participants'),
        select: (res) => res.participants,
    });

    useEffect(() => {
        if (isError) {
            console.error(error);
            alert(error);
        }
    }, [isError, error]);

    return (
        <Fragment>
            <Helmet>
                <title>Participants - Admin Dashboard</title>
            </Helmet>
            <div className={cn('min-h-screen p-8', Styles.backgrounds.primaryGradient)}>
                <div className="max-w-[95vw] mx-auto">
                    <Link to="/admin/dashboard">
                        <Button variant="ghost" className={cn('mb-6', Styles.glass.ghostButton)}>
                            {BACK_BUTTON}
                        </Button>
                    </Link>

                    <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-8">
                        <div>
                            <h1 className={cn('text-4xl', Styles.text.title)}>Participants</h1>
                            <p className={Styles.text.subtitle}>View all hackathon participants</p>
                        </div>
                    </div>

                    {isLoading ? (
                        <Card className={cn('p-20 text-center border-dashed', Styles.glass.card)}>
                            <p className={cn('text-xl font-medium', Styles.text.subtitle)}>Loading participants...</p>
                        </Card>
                    ) : data && data.length > 0 ? (
                        <DataTable columns={columns} data={data} />
                    ) : (
                        <Card className={cn('p-20 text-center border-dashed', Styles.glass.card)}>
                            <p className={cn('text-xl font-medium', Styles.text.subtitle)}>No participants found</p>
                        </Card>
                    )}
                </div>
            </div>
        </Fragment>
    );
}
