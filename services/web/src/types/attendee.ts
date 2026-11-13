export type TicketType = 'GUEST' | 'PARTICIPANT';

export type Attendee = {
    id: string;
    name: string;
    email: string;
    ticket_type: TicketType;
    has_paid: boolean;
    // Set by the backend once the ticket has been created and emailed
    ticket_serial_number: string | null;
};
