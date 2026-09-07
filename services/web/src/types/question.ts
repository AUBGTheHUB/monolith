export type Question = {
    id: string;
    prompt: string;
    // fix types
    question_type: [];
    answer_type: [];
    options: string | undefined;
};
