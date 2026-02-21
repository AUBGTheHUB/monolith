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
            { label: 'UI/UX Design', points: 8 },
            { label: 'Scalability', points: 5 },
            { label: 'Structured git repository with documentation', points: 2 },
            { label: 'Project deployment', points: 2 },
        ],
    },
};


export const bottomRowData: { left: GradingCategory; right: GradingCategory } = {
    left: {
        title: 'COMPLEXITY OF THE PROJECT',
        items: [
            { label: 'Code originality', points: 8 },
            { label: 'Suitable technology stack', points: 5 },
            { label: 'Clear coding style', points: 2 },
            { label: 'Security', points: 2 },
        ],
    },
    right: {
        title: 'PRESENTATION',
        items: [
            { label: 'Coherency', points: 8 },
            { label: 'Clear explanation and defense of project ideas', points: 5 },
            { label: 'Demo', points: 2 },
            { label: 'Demonstration and explanation of the most complex feature of the project', points: 2 },
        ],
    },
};
