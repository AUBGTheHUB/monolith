import { GradingCategory } from "./types";

export const topRowData: {left: GradingCategory; right: GradingCategory} = {
    left: {
        title: 'PROJECT IDEA',
        items: [
            { label: 'Innovative idea and originality', points: 8},
            { label: 'Market research', points: 5},
            { label: 'Usage of external data to verify the idea', points: 2},
        ],

    },
    right: {
        title: 'PROJECT REALIZATION',
        items: [
            { label: 'UI/UX Design', points: 10 },
            { label: 'Scalability', points: 10 },
            { label: 'Structured git repository with documentation', points: 5 },
            { label: 'Project deployment', points: 5 },
        ],
    },
};


export const bottomRowData: { left: GradingCategory; right: GradingCategory } = {
    left: {
        title: 'COMPLEXITY OF THE PROJECT',
        items: [
            { label: 'Code originality', points: 15 },
            { label: 'Suitable technology stack', points: 10 },
            { label: 'Clear coding style', points: 10 },
            { label: 'Security', points: 5 },
        ],
    },
    right: {
        title: 'PRESENTATION',
        items: [
            { label: 'Coherency', points: 15 },
            { label: 'Clear explanation and defense of project ideas', points: 10 },
            { label: 'Demo', points: 10 },
            { label: 'Demonstration and explanation of the most complex feature of the project', points: 5 },
        ],
    },
};
