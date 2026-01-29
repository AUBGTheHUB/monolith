export const SponsorsPageMessages = {
    PAGE_TITLE: 'Sponsors - Admin Dashboard',
    HEADING: 'Sponsors',
    SUBTITLE: 'Manage hackathon sponsorships and partnerships',
    BACK_BUTTON: (
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
    ),
    ADD_BUTTON: (
        <span className="flex items-center gap-2">
            <svg
                xmlns="http://www.w3.org/2000/svg"
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="icon icon-tabler icons-tabler-outline icon-tabler-layout-grid-add"
            >
                <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                <path d="M4 5a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1l0 -4" />
                <path d="M14 5a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1l0 -4" />
                <path d="M4 15a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1l0 -4" />
                <path d="M14 17h6m-3 -3v6" />
            </svg>
            Add New Sponsor
        </span>
    ),
    EMPTY_STATE: 'No sponsors added yet. Click "Add New Sponsor" to get started.',
    DELETE_CONFIRM: (name: string) => `Are you sure you want to delete ${name}?`,
    EDIT_BUTTON: 'Edit',
    DELETE_BUTTON: 'Delete',
};

export const SponsorsEditMessages = {
    PAGE_TITLE: 'Edit Sponsor - Admin Dashboard',
    NOT_FOUND_TITLE: 'Sponsor Not Found - Admin Dashboard',
    HEADING: 'Edit Sponsor',
    SUBTITLE: 'Update sponsor information',
    BACK_BUTTON: (
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
            Back to Sponsors
        </span>
    ),
    NOT_FOUND_MESSAGE: 'Sponsor not found',
    RETURN_BUTTON: 'Return to Sponsors List',
    CANCEL_BUTTON: 'Cancel',
    SUBMIT_BUTTON: 'Update Sponsor',
    SUCCESS_MESSAGE: 'Sponsor updated successfully! (Mock)',
};

export const SponsorsAddMessages = {
    PAGE_TITLE: 'Add Sponsor - Admin Dashboard',
    HEADING: 'Add New Sponsor',
    SUBTITLE: 'Fill in the details to add a new sponsor',
    BACK_BUTTON: (
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
            </svg>{' '}
            Back to Sponsors
        </span>
    ),
    CANCEL_BUTTON: 'Cancel',
    SUBMIT_BUTTON: 'Add Sponsor',
    SUCCESS_MESSAGE: 'Sponsor added successfully!',
};

export const SponsorsFormFieldMessages = {
    LABELS: {
        NAME: 'Sponsor Name',
        TIER: 'Badge/Tier',
        LOGO: 'Logo URL',
        WEBSITE: 'Website URL',
        CAREERS: 'Careers Page URL',
    },
    PLACEHOLDERS: {
        NAME: "Enter sponsor's name",
        TIER: 'Enter tier (e.g., Gold, Silver, Partner)',
        LOGO: 'Enter logo URL (e.g., /logos/sponsor.png)',
        WEBSITE: 'Enter main website URL',
        CAREERS: 'Enter careers page URL (optional)',
    },
};

export const ERROR_MESSAGES = {
    FAILED_DELETE: 'Failed to delete sponsor. Contact dev',
    FAILED_SAVE: 'An error occurred while saving.',
};
