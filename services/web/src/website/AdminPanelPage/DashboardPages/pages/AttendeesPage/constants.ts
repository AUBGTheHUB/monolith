import type { Attendee } from '@/types/attendee.ts';

export const ATTENDEES_ENDPOINT = '/attendees';
export const ATTENDEES_ROUTE = '/admin/dashboard/gaming-event-attendees';
export const ATTENDEES_QUERY_KEY = 'gaming-event-attendees';

export const hasTicketBeenSent = (attendee: Attendee): boolean => Boolean(attendee.ticket_serial_number);
