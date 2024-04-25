module.exports = {
    root: true,
    env: {
        node: true,
        browser: true,
        es2020: true,
    },
    extends: [
        'eslint:recommended',
        'plugin:unicorn/recommended',
        'plugin:prettier/recommended',
        'plugin:functional/recommended',
        'plugin:functional/no-other-paradigms',
        'plugin:functional/stylistic',
        'plugin:functional/disable-type-checked',
    ],
    plugins: [
        'functional',
        'simple-import-sort',
        'unused-imports',
        'prefer-arrow-functions',
        'react',
        'react-hooks',
        'react-refresh',
    ],
    rules: {
        'unicorn/prevent-abbreviations': 'off',
        'unicorn/filename-case': 'off',
        'unicorn/no-array-callback-reference': 'off',
        'prefer-template': 'error',
        'no-console': 'error',
        'object-shorthand': 'error',
        'simple-import-sort/imports': 'error',
        'unused-imports/no-unused-imports': 'error',
        'unused-imports/no-unused-vars': [
            'error',
            {
                vars: 'all',
                varsIgnorePattern: '^_',
                args: 'after-used',
                argsIgnorePattern: '^_',
            },
        ],
    },
    ignorePatterns: ['__generated__'],
    overrides: [
        {
            files: ['*.ts', '*.tsx'],
            extends: [
                'plugin:@typescript-eslint/recommended',
                'plugin:@typescript-eslint/recommended-requiring-type-checking',
                'plugin:functional/recommended',
                'plugin:functional/no-other-paradigms',
                'plugin:functional/stylistic',
                'plugin:functional/external-typescript-recommended',
            ],
            parserOptions: {
                project: true,
            },
            rules: {
                'functional/functional-parameters': 'off',
                'functional/prefer-immutable-types': 'off',
                'functional/no-expression-statements': 'off',
                'functional/no-mixed-types': 'off',
                'react/jsx-curly-brace-presence': [
                    'error',
                    { props: 'always', children: 'never' },
                ],
                'react/react-in-jsx-scope': 'off',
                'react/jsx-uses-react': 'off',
                'react/prop-types': 0,
                'react-hooks/rules-of-hooks': 'error',
                'react/display-name': 'off',
                'react/jsx-no-bind': 'warn',
                'react-hooks/exhaustive-deps': 'error',
                'prefer-arrow-functions/prefer-arrow-functions': [
                    'warn',
                    {
                        allowNamedFunctions: false,
                        classPropertiesAllowed: false,
                        disallowPrototype: false,
                        returnStyle: 'unchanged',
                        singleReturnOnly: false,
                    },
                ],
            },
        },
    ],
    settings: {
        react: {
            version: 'detect',
        },
    },
}
