import { createContext, useState, useEffect, type PropsWithChildren } from "react";
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Uniwind, useUniwind } from "uniwind";


const lightThemeKey = 'light';
const darkThemeKey = 'dark';
const themeKey = 'appTheme';

type ThemeType = typeof lightThemeKey | typeof darkThemeKey;
type ThemeContextType = {
    theme: ThemeType;
    toggleTheme: () => void;
}

export const ThemeContext = createContext<ThemeContextType>({
    theme: lightThemeKey,
    toggleTheme: () => {}
});


export function ThemeProvider({ children }: PropsWithChildren) {
   const {theme} = useUniwind();

    useEffect(() => {
        loadSavedTheme();
    }, []);

    const loadSavedTheme = async () => {
        try {
            const savedTheme = await AsyncStorage.getItem(themeKey);

            if (savedTheme === lightThemeKey || savedTheme === darkThemeKey) {
                Uniwind.setTheme(savedTheme);
            } else {
                Uniwind.setTheme(theme)
            }
        } catch (error) {
            console.error('Failed to load theme:', error);
        }
    }

    const toggleTheme = async () => {
        const newTheme = theme === lightThemeKey ? darkThemeKey : lightThemeKey;
        Uniwind.setTheme(newTheme);

        try {
            await AsyncStorage.setItem(themeKey, newTheme);
        } catch (error) {
            console.error('Failed to save theme:', error);
        }
    }

    return (
        <ThemeContext.Provider value={{ theme, toggleTheme }}>
            {children}
        </ThemeContext.Provider>
    )
}