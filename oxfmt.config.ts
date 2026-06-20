import { defineConfig } from 'oxfmt';

// TODO: remove frontend from ignorepatterns

export default defineConfig({
  semi: true,
  singleQuote: true,
  jsxSingleQuote: true,
  sortPackageJson: true,
  sortImports: {
    groups: [
      "type-import",
      ["value-builtin", "value-external"],
      "type-internal",
      "value-internal",
      ["type-parent", "type-sibling", "type-index"],
      ["value-parent", "value-sibling", "value-index"],
      "unknown",
    ],
  },
  sortTailwindcss: {
    stylesheet: "./global.css",
    functions: ["clsx", "cn", "tv"],
    preserveWhitespace: true,
  },
  ignorePatterns: [
    "backend/**",
    "frontend/**"
  ]
});
