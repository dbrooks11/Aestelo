import { defineConfig } from 'oxlint';
import baseConfig from '../../oxlint.config.ts'; 

export default defineConfig({
  extends: [baseConfig],
  jsPlugins: [
    {
      name: 'react-native',
      specifier: 'eslint-plugin-react-native'
    }
  ],
  env: {
    es6: true
  },
  globals: {
    __DEV__: 'readonly'
  },
  rules: {
    'react-native/no-unused-styles': 'error',
    'react-native/no-inline-styles': 'warn',
    'react-native/no-raw-text': 'error',
    'react-native/no-single-element-style-arrays': 'error',
    'react-native/no-color-literals': 'warn',
    'react-native/sort-styles': 'off'
  }
});
