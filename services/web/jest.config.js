/** @type {import('ts-jest').JestConfigWithTsJest} **/
export default {
    testEnvironment: 'jsdom',
    transform: {
        '^.+\\.(js|jsx|ts|tsx)$': ['babel-jest', {}],
    },
};
