module.exports = {
    presets: [
        '@babel/preset-env', // for JavaScript (ES6+)
        '@babel/preset-typescript', // for TypeScript
        ['@babel/preset-react',
            {
                runtime: 'automatic',
            }]
    ],
    plugins: [
        // Optional: Add any other plugins you need
    ],
};
