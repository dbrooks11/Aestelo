import { defineConfig } from 'oxlint';

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
    "test/snapshots/**"
  ]
});
