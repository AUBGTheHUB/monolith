const BackIcon = () => (
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
);

const AddIcon = () => (
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
        className="icon icon-tabler icons-tabler-outline icon-tabler-user-plus"
    >
        <path stroke="none" d="M0 0h24v24H0z" fill="none" />
        <path d="M8 7a4 4 0 1 0 8 0a4 4 0 0 0 -8 0" />
        <path d="M16 19h6" />
        <path d="M19 16v6" />
        <path d="M6 21v-2a4 4 0 0 1 4 -4h4" />
    </svg>
);

export const AttendeesPageMessages = {
    PAGE_TITLE: 'Gaming Event Attendees - Admin Dashboard',
    HEADING: 'Gaming Event Attendees',
    SUBTITLE: 'Manage attendees, payments and tickets for the gaming event',
    BACK_BUTTON: (
        <span className="flex items-center gap-1">
            <BackIcon />
            Back to Dashboard
        </span>
    ),
    ADD_BUTTON: (
        <span className="flex items-center gap-2">
            <AddIcon />
            Add New Attendee
        </span>
    ),
    EMPTY_STATE: 'No attendees added yet. Click "Add New Attendee" to get started.',
    LOADING_STATE: 'Loading attendees, please wait...',
    DELETE_CONFIRM: (name: string) => `Are you sure you want to delete ${name}? This cannot be undone.`,
    SEND_TICKET_CONFIRM: (name: string, email: string) => `Send the ticket to ${name} (${email})?`,
    SEND_TICKET_SUCCESS: (name: string) => `Ticket sent to ${name}.`,
    EDIT_BUTTON: 'Edit',
    DELETE_BUTTON: 'Delete',
    SEND_TICKET_BUTTON: 'Send Ticket',
    SENDING_TICKET_BUTTON: 'Sending...',
    TICKET_TYPE_LABELS: {
        guest: 'Guest',
        participant: 'Participant',
    },
    PAID: 'Paid',
    NOT_PAID: 'Not paid',
};

export const AttendeesEditMessages = {
    PAGE_TITLE: 'Edit Attendee - Admin Dashboard',
    NOT_FOUND_TITLE: 'Attendee Not Found - Admin Dashboard',
    HEADING: 'Edit Attendee',
    SUBTITLE: 'Fix attendee information that was entered incorrectly',
    BACK_BUTTON: (
        <span className="flex items-center gap-1">
            <BackIcon />
            Back to Attendees
        </span>
    ),
    NOT_FOUND_MESSAGE: 'Attendee not found',
    RETURN_BUTTON: 'Return to Attendees List',
    CANCEL_BUTTON: 'Cancel',
    SUBMIT_BUTTON: 'Update Attendee',
    SUBMITTING_BUTTON: 'Saving...',
    LOADING_STATE: 'Loading attendee, please wait...',
};

export const AttendeesAddMessages = {
    PAGE_TITLE: 'Add Attendee - Admin Dashboard',
    HEADING: 'Add New Attendee',
    SUBTITLE: 'Fill in the details to add a new attendee',
    BACK_BUTTON: (
        <span className="flex items-center gap-1">
            <BackIcon />
            Back to Attendees
        </span>
    ),
    CANCEL_BUTTON: 'Cancel',
    SUBMIT_BUTTON: 'Add Attendee',
    SUBMITTING_BUTTON: 'Saving...',
};

export const AttendeesFormFieldMessages = {
    LABELS: {
        NAME: 'Name',
        EMAIL: 'Email',
        TICKET_TYPE: 'Ticket Type',
        HAS_PAID: 'Has the attendee paid for their ticket?',
    },
    PLACEHOLDERS: {
        NAME: "Enter attendee's full name",
        EMAIL: 'Enter attendee email (e.g., name@example.com)',
    },
    TICKET_TYPE_OPTIONS: [
        { label: 'Guest', value: 'guest' },
        { label: 'Participant', value: 'participant' },
    ],
    HAS_PAID_OPTIONS: [
        { label: 'Yes', value: true },
        { label: 'No', value: false },
    ],
};
