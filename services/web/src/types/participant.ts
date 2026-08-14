export interface Participant {
    id: string;
    name: string;
    email: string;
    is_admin: boolean;
    email_verified: boolean;
    team_id: string | null;
    team_name: string | null;
    tshirt_size: string | null;
    university: string;
    location: string;
    age: number;
    source_of_referral: string | null;
    programming_language: string | null;
    programming_level: string | null;
    has_participated_in_hackaubg: boolean;
    has_internship_interest: boolean;
    has_participated_in_hackathons: boolean;
    has_previous_coding_experience: boolean;
    share_info_with_sponsors: boolean;
    created_at: string;
    updated_at: string;
    last_sent_verification_email: string | null;
}
