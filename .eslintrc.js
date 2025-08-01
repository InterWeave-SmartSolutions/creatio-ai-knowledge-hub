module.exports = {
  root: true,
  env: {
    browser: true,
    es2021: true,
    node: true,
    jest: true
  },
  extends: [
    'eslint:recommended'
  ],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module'
  },
  rules: {
    // General JavaScript rules
    'no-console': 'warn',
    'no-debugger': 'warn',
    'no-unused-vars': ['error', { 
      argsIgnorePattern: '^_',
      varsIgnorePattern: '^_'
    }],
    
    // Code quality rules
    'prefer-const': 'error',
    'no-var': 'error',
    'object-shorthand': 'error',
    'prefer-template': 'error',
    'prefer-arrow-callback': 'error',
    
    // Creatio platform specific rules
    'no-eval': 'error',
    'no-implied-eval': 'error',
    'no-new-func': 'error'
  },
  overrides: [
    {
      files: ['*.test.js', '*.test.ts', '*.spec.js', '*.spec.ts'],
      env: {
        jest: true
      },
      rules: {
        'no-console': 'off'
      }
    }
  ],
  ignorePatterns: [
    'node_modules/',
    'dist/',
    'build/',
    'bin/',
    'obj/',
    '*.min.js',
    'coverage/',
    '.vscode/',
    '.git/',
    'config/',
    'backup/',
    'creatio-academy-archive/',
    'transcriptions/'
  ]
};
