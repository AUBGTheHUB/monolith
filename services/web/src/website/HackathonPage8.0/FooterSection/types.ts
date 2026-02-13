export type FooterLink = {
    label: string;
    href?: string;
};

export type FooterColumn = {
    id: number;
    title: string;
    items: FooterLink[];
};