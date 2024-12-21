/** @type {import('ts-jest').JestConfigWithTsJest} **/
export default {
    testEnvironment: 'jsdom',
    moduleNameMapper: {
        '^@/(.*)$': '<rootDir>/src/$1',
    },
    transform: {
        '^.+\\.(js|jsx|ts|tsx)$': ['babel-jest', {}],
    },
};