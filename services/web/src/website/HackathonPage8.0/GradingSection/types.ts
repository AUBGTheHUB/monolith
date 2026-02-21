export type GradingItem = {
    label: string;
    points: number;
};

export type GradingCategory = {
    title: string;
    items: GradingItem[];
};
