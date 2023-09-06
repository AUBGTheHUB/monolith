import type { Question } from '$lib/inputs/types';

export type DepartmentQuestions = {
    _id: string;
    department: string;
    questions: Question[];
};
