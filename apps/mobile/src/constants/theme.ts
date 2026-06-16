/**
 * Below are the colors that are used in the app. The colors are defined in the light and dark mode.
 * There are many other ways to style your app. For example, [Nativewind](https://www.nativewind.dev/), [Tamagui](https://tamagui.dev/), [unistyles](https://reactnativeunistyles.vercel.app), etc.
 */
import { Platform } from 'react-native';

export const themes = {
  light: {
    textPrimary: '#C85A5E',
    background: '#ffffff',
    backgroundElement: '#F0F0F3',
    backgroundSelected: '#E0E1E6',
    textSecondary: '#000000',
  },
  dark: {
    textPrimary: '#FFFFFF',
    background: '#1a1a1a',
    backgroundElement: '#212225',
    backgroundSelected: '#2E3135',
    textSecondary: '#FFFFFF',
    textSecondaryMuted: '#737373'
  },
} as const;

export type ThemeColor = keyof typeof themes.light & keyof typeof themes.dark;

export const Fonts = Platform.select({
  ios: {
    /** iOS `UIFontDescriptorSystemDesignDefault` */
    sans: 'system-ui',
    /** iOS `UIFontDescriptorSystemDesignSerif` */
    serif: 'ui-serif',
    /** iOS `UIFontDescriptorSystemDesignRounded` */
    rounded: 'ui-rounded',
    /** iOS `UIFontDescriptorSystemDesignMonospaced` */
    mono: 'ui-monospace',
  },
  default: {
    sans: 'normal',
    serif: 'serif',
    rounded: 'normal',
    mono: 'monospace',
  },
});

export const spacing = {
  half: 2,
  one: 4,
  two: 8,
  three: 16,
  four: 24,
  five: 32,
  six: 64,
} as const;

export const fontSize = {
  one: 4,
  two: 8,
  three: 12,
  four: 16,
  five: 20,
  six: 24,
  seven: 28,
  eight: 32,
  nine: 64
}

export const BottomTabInset = Platform.select({ ios: 50, android: 80 }) ?? 0;
export const MaxContentWidth = 800;