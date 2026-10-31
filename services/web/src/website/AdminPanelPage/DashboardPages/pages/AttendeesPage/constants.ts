import type { Attendee } from '@/types/attendee.ts';

export const ATTENDEES_ENDPOINT = '/gaming-event/attendees';
export const ATTENDEES_ROUTE = '/admin/dashboard/gaming-event-attendees';
export const ATTENDEES_QUERY_KEY = 'gaming-event-attendees';

// The ticket doesn't specify the GET response shape yet, so accept either
// `{ attendees: [...] }` (like the other admin endpoints) or a plain array.
export const unwrapAttendees = (res: { attendees: Attendee[] } | Attendee[]): Attendee[] =>
    Array.isArray(res) ? res : res.attendees;

export const unwrapAttendee = (res: { attendee: Attendee } | Attendee): Attendee =>
    'attendee' in res ? res.attendee : res;
