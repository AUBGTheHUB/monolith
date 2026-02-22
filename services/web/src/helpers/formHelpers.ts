/**
 * Converts a plain object into a FormData object.
 * Handles FileList (from inputs), Files, and standard primitive values.
 */
export const toFormData = <T extends Record<string, unknown>>(data: T): FormData => {
    const formData = new FormData();

    Object.entries(data).forEach(([key, value]) => {
        // 1. Handle FileList (multiple or single files from a browser input)
        if (value instanceof FileList) {
            Array.from(value).forEach((file) => formData.append(key, file));
        }
        // 2. Handle single File or Blob objects
        else if (value instanceof File) {
            formData.append(key, value);
        }
        // 3. Handle Arrays (not files) - FastAPI often expects multiple entries for the same key
        else if (Array.isArray(value)) {
            value.forEach((v) => formData.append(key, v));
        }
        // 4. Handle standard primitives (strings, numbers, booleans)
        else if (value !== null && value !== undefined) {
            // Convert numbers/booleans to string for FormData
            formData.append(key, value.toString());
        }
    });

    return formData;
};
