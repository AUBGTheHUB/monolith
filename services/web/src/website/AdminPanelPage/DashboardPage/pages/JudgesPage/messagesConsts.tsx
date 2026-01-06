export const JudgesPageMessages = {
    PAGE_TITLE: 'Judges - Admin Dashboard',
    HEADING: 'Judges',
    SUBTITLE: 'Manage hackathon judges',
    BACK_BUTTON: '← Back to Dashboard',
    ADD_BUTTON: '+ Add New Judge',
    EMPTY_STATE: 'No judges added yet. Click "Add New Judge" to get started.',
    DELETE_CONFIRM: (name: string) => `Are you sure you want to delete ${name}?`,
    EDIT_BUTTON: 'Edit',
    DELETE_BUTTON: 'Delete',
};

export const JudgesEditMessages = {
    PAGE_TITLE: 'Edit Judge - Admin Dashboard',
    NOT_FOUND_TITLE: 'Judge Not Found - Admin Dashboard',
    HEADING: 'Edit Judge',
    SUBTITLE: 'Update judge information',
    BACK_BUTTON: '← Back to Judges',
    NOT_FOUND_MESSAGE: 'Judge not found',
    RETURN_BUTTON: 'Return to Judges List',
    CANCEL_BUTTON: 'Cancel',
    SUBMIT_BUTTON: 'Update Judge',
    SUCCESS_MESSAGE: 'Judge updated successfully! (This is a mock - no API call made)',
};

export const JudgesAddMessages = {
    PAGE_TITLE: 'Add Judge - Admin Dashboard',
    HEADING: 'Add New Judge',
    SUBTITLE: 'Fill in the details to add a new judge',
    BACK_BUTTON: '← Back to Judges',
    CANCEL_BUTTON: 'Cancel',
    SUBMIT_BUTTON: 'Add Judge',
    SUCCESS_MESSAGE: 'Judge added successfully!',
};

export const JudgesFormFieldMessages = {
    LABELS: {
        NAME: 'Name',
        COMPANY: 'Company Name',
        IMAGE: 'Image URL',
    },
    PLACEHOLDERS: {
        NAME: "Enter judge's full name",
        COMPANY: 'Enter company name',
        IMAGE: 'Enter image URL (e.g., /judge_photo.webp)',
    },
};
