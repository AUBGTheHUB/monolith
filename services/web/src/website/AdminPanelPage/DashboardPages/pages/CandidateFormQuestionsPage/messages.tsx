export const CandidateFormQuestionMessages = {
    PAGE_TITLE: 'Candidate Form Questions - Admin Dashboard',
    HEADING: 'Candidate Form Questions',
    SUBTITLE: 'Manage the questions for new applicants',
    BACK_BUTTON: (
        <span className="flex items-center gap-1">
            <svg
                xmlns="http://www.w3.org/2000/svg"
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="currentColor"
                className="icon icon-tabler icons-tabler-filled icon-tabler-caret-left"
            >
                <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                <path d="M13.883 5.007l.058 -.005h.118l.058 .005l.06 .009l.052 .01l.108 .032l.067 .027l.132 .07l.09 .065l.081 .073l.083 .094l.054 .077l.054 .096l.017 .036l.027 .067l.032 .108l.01 .053l.01 .06l.004 .057l.002 .059v12c0 .852 -.986 1.297 -1.623 .783l-.084 -.076l-6 -6a1 1 0 0 1 -.083 -1.32l.083 -.094l6 -6l.094 -.083l.077 -.054l.096 -.054l.036 -.017l.067 -.027l.108 -.032l.053 -.01l.06 -.01z" />
            </svg>
            Back to Dashboard
        </span>
    ),
    ADD_BUTTON: (
        <span className="flex items-center gap-2">
            <svg
                xmlns="http://www.w3.org/2000/svg"
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="icon icon-tabler icons-tabler-outline icon-tabler-layout-grid-add"
            >
                <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                <path d="M4 5a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1l0 -4" />
                <path d="M14 5a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1l0 -4" />
                <path d="M4 15a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1l0 -4" />
                <path d="M14 17h6m-3 -3v6" />
            </svg>
            Add New Question
        </span>
    ),
    EMPTY_STATE: 'No questions added yet. Click "Add New Question" to get started.',
    LOADING_STATE: 'Loading questions, please wait...',
    DELETE_CONFIRM: (prompt: string) => `Are you sure you want to delete ${prompt}?`,
    EDIT_BUTTON: 'Edit',
    DELETE_BUTTON: 'Delete',
};

export const CandidateFormQuestionEditMessages = {
    PAGE_TITLE: 'Edit Question - Admin Dashboard',
    NOT_FOUND_TITLE: 'Question Not Found - Admin Dashboard',
    HEADING: 'Edit Questioj',
    SUBTITLE: 'Update Question',
    BACK_BUTTON: (
        <span className="flex items-center gap-1">
            <svg
                xmlns="http://www.w3.org/2000/svg"
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="currentColor"
                className="icon icon-tabler icons-tabler-filled icon-tabler-caret-left"
            >
                <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                <path d="M13.883 5.007l.058 -.005h.118l.058 .005l.06 .009l.052 .01l.108 .032l.067 .027l.132 .07l.09 .065l.081 .073l.083 .094l.054 .077l.054 .096l.017 .036l.027 .067l.032 .108l.01 .053l.01 .06l.004 .057l.002 .059v12c0 .852 -.986 1.297 -1.623 .783l-.084 -.076l-6 -6a1 1 0 0 1 -.083 -1.32l.083 -.094l6 -6l.094 -.083l.077 -.054l.096 -.054l.036 -.017l.067 -.027l.108 -.032l.053 -.01l.06 -.01z" />
            </svg>
            Back to Questions
        </span>
    ),
    NOT_FOUND_MESSAGE: 'Question not found',
    RETURN_BUTTON: 'Return to Question List',
    CANCEL_BUTTON: 'Cancel',
    SUBMIT_BUTTON: 'Update Question',
    LOADING_STATE: 'Loading Question, please wait...',
};

export const CandidateFormQuestionAddMessages = {
    PAGE_TITLE: 'Add Question - Admin Dashboard',
    HEADING: 'Add New Question',
    SUBTITLE: 'Fill in the details to add a new question',
    BACK_BUTTON: (
        <span className="flex items-center gap-1">
            <svg
                xmlns="http://www.w3.org/2000/svg"
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="currentColor"
                className="icon icon-tabler icons-tabler-filled icon-tabler-caret-left"
            >
                <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                <path d="M13.883 5.007l.058 -.005h.118l.058 .005l.06 .009l.052 .01l.108 .032l.067 .027l.132 .07l.09 .065l.081 .073l.083 .094l.054 .077l.054 .096l.017 .036l.027 .067l.032 .108l.01 .053l.01 .06l.004 .057l.002 .059v12c0 .852 -.986 1.297 -1.623 .783l-.084 -.076l-6 -6a1 1 0 0 1 -.083 -1.32l.083 -.094l6 -6l.094 -.083l.077 -.054l.096 -.054l.036 -.017l.067 -.027l.108 -.032l.053 -.01l.06 -.01z" />
            </svg>{' '}
            Back to Questions
        </span>
    ),
    CANCEL_BUTTON: 'Cancel',
    SUBMIT_BUTTON: 'Add Question',
};

export const CandidateFormQuestionFormFieldMessages = {
    LABELS: {
        PROMPT: 'Prompt',
        QUESTIONTYPE: 'Question Type',
        ANSWERTYPE: 'Avatar Image',
        OPTIONS: 'Options',
    },
    PLACEHOLDERS: {
        NAME: 'What do you want to ask the applicant?',
        QUESTIONTYPE: 'Which department is the question about?',
        ANSWERTYPE: 'What answer type is the question?',
        OPTIONS: 'Give the different options, separated my comma',
    },
};
