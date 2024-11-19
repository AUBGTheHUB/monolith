import globals from 'globals';
import pluginJs from '@eslint/js';
import jestPlugin from 'eslint-plugin-jest';
import tseslint from 'typescript-eslint';
import pluginReact from 'eslint-plugin-react';
import pluginUnusedImports from 'eslint-plugin-unused-imports';

export default [
    { files: ['**/*.{js,mjs,cjs,ts,jsx,tsx}'] },
    { languageOptions: { globals: globals.browser } },
    pluginJs.configs.recommended,
    ...tseslint.configs.recommended,
    pluginReact.configs.flat.recommended,
    {
        plugins: {
            'unused-imports': pluginUnusedImports,
        },
        rules: {
            'react/react-in-jsx-scope': 'off',
            'unused-imports/no-unused-imports': 'warn',
            'unused-imports/no-unused-vars': [
                'warn',
                { vars: 'all', varsIgnorePattern: '^_', args: 'after-used', argsIgnorePattern: '^_' },
            ],
        },
    },
    {
        files: ['**/components/ui/*.tsx'],
        rules: {
            'react/prop-types': [2, { ignore: ['className'] }],
            'react-refresh/only-export-components': 'off',
        },
    },
  {
    files: ['*.js', '*.jsx', '*.ts', '*.tsx'],
    plugins: {
      jest: jestPlugin, // Register the Jest plugin
    },
    languageOptions: {
      parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module',
      },
    },
        rules: {
            'jest/no-disabled-tests': 'warn',
            'jest/no-focused-tests': 'error',
            'jest/no-identical-title': 'error',
            'jest/prefer-to-have-length': 'warn',
            'jest/valid-expect': 'error',
        },
    }
];
