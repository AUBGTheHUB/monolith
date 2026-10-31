export type TicketType = 'guest' | 'participant';

export type Attendee = {
    id: string;
    name: string;
    email: string;
    ticket_type: TicketType;
    has_paid: boolean;
    created_at?: string;
    updated_at?: string;
};
