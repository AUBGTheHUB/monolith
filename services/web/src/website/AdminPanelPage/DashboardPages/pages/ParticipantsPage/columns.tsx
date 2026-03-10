import { ColumnDef } from '@tanstack/react-table';
import { ArrowUpDown } from 'lucide-react';
import { Button } from '@/components/ui/button';
import type { Participant } from '@/types/participant';

function renderCellValue(value: unknown): string {
    if (value === null || value === undefined) return '—';
    if (typeof value === 'boolean') return value ? 'Yes' : 'No';
    return String(value);
}

export const columns: ColumnDef<Participant>[] = [
    {
        accessorKey: 'name',
        header: 'Name',
        cell: ({ row }) => renderCellValue(row.getValue('name')),
    },
    {
        accessorKey: 'email',
        header: 'Email',
        cell: ({ row }) => renderCellValue(row.getValue('email')),
    },
    {
        accessorKey: 'is_admin',
        header: 'Is Admin',
        cell: ({ row }) => renderCellValue(row.getValue('is_admin')),
    },
    {
        accessorKey: 'email_verified',
        header: 'Email Verified',
        cell: ({ row }) => renderCellValue(row.getValue('email_verified')),
    },
    {
        // Each participant stores a team_id (ObjectId reference to the teams collection).
        // The backend handler fetches all teams, builds a team_id → team_name map,
        // and injects the resolved team_name into each participant's JSON response.
        // Participants without a team (team_id is null) will have team_name as null, displayed as "—".
        accessorKey: 'team_name',
        header: ({ column }) => (
            <Button variant="ghost" onClick={() => column.toggleSorting(column.getIsSorted() === 'asc')}>
                Team Name
                <ArrowUpDown className="ml-2 h-4 w-4" />
            </Button>
        ),
        cell: ({ row }) => renderCellValue(row.getValue('team_name')),
        sortingFn: (rowA, rowB) => {
            const a = rowA.getValue('team_name') as string | null;
            const b = rowB.getValue('team_name') as string | null;
            if (a === null && b === null) return 0;
            if (a === null) return 1;
            if (b === null) return -1;
            return a.localeCompare(b);
        },
    },
    {
        accessorKey: 'tshirt_size',
        header: 'T-Shirt Size',
        cell: ({ row }) => renderCellValue(row.getValue('tshirt_size')),
    },
    {
        accessorKey: 'university',
        header: 'University',
        cell: ({ row }) => renderCellValue(row.getValue('university')),
    },
    {
        accessorKey: 'location',
        header: 'Location',
        cell: ({ row }) => renderCellValue(row.getValue('location')),
    },
    {
        accessorKey: 'age',
        header: 'Age',
        cell: ({ row }) => renderCellValue(row.getValue('age')),
    },
    {
        accessorKey: 'source_of_referral',
        header: 'Source of Referral',
        cell: ({ row }) => renderCellValue(row.getValue('source_of_referral')),
    },
    {
        accessorKey: 'programming_language',
        header: 'Programming Language',
        cell: ({ row }) => renderCellValue(row.getValue('programming_language')),
    },
    {
        accessorKey: 'programming_level',
        header: 'Programming Level',
        cell: ({ row }) => renderCellValue(row.getValue('programming_level')),
    },
    {
        accessorKey: 'has_participated_in_hackaubg',
        header: 'Participated in HackAUBG',
        cell: ({ row }) => renderCellValue(row.getValue('has_participated_in_hackaubg')),
    },
    {
        accessorKey: 'has_internship_interest',
        header: 'Internship Interest',
        cell: ({ row }) => renderCellValue(row.getValue('has_internship_interest')),
    },
    {
        accessorKey: 'has_participated_in_hackathons',
        header: 'Participated in Hackathons',
        cell: ({ row }) => renderCellValue(row.getValue('has_participated_in_hackathons')),
    },
    {
        accessorKey: 'has_previous_coding_experience',
        header: 'Previous Coding Experience',
        cell: ({ row }) => renderCellValue(row.getValue('has_previous_coding_experience')),
    },
    {
        accessorKey: 'share_info_with_sponsors',
        header: 'Share Info with Sponsors',
        cell: ({ row }) => renderCellValue(row.getValue('share_info_with_sponsors')),
    },
];
