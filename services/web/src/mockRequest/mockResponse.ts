// src/test.ts

export type MockData = {
    data: string;
};

export const fetchMockData = async (): Promise<MockData> => {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            // Simulate a random error
            const shouldThrowError = Math.random() > 0.5;
            if (shouldThrowError) {
                reject(new Error('Something went wrong!'));
            } else {
                resolve({ data: 'Hello from React Query!' });
            }
        }, 1000);
    });
};
