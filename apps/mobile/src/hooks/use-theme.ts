/**
 * Learn more about light and dark modes:
 * https://docs.expo.dev/guides/color-schemes/
 */

import { ThemeContext } from '@/context/theme-ctx';
import { useContext } from 'react';


export function useTheme() {
  const context = useContext(ThemeContext);

  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  const {theme, toggleTheme} = context

  return {
    theme,
    toggleTheme,
  }
}
