import { defineConfig } from 'oxlint';

// TODO: remove frontend from ignorePatterns

export default defineConfig({
  plugins: ['eslint', 'typescript', 'unicorn', 'oxc'],
  categories: {
    correctness: 'error',
    suspicious: 'warn',
    pedantic: 'off',
  },
  ignorePatterns: [
    '**/dist/**',
    '**/build/**',
    '**/.expo/**',
    '**/node_modules/**',
    '**/coverage/**',
    '**/.turbo/**',
    "vendor/**",
    "test/snapshots/**",
    "frontend/**"
  ]
});
