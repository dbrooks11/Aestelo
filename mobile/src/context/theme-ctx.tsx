import { createContext, useState, useEffect, type PropsWithChildren } from "react";
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useColorScheme } from "react-native";


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
    const systemColorScheme = useColorScheme();
    const [theme, setTheme] = useState<ThemeType>(lightThemeKey);

    useEffect(() => {
        loadSavedTheme();
    }, []);

    const loadSavedTheme = async () => {
        try {
            const savedTheme = await AsyncStorage.getItem(themeKey);

            if (savedTheme === lightThemeKey || savedTheme === darkThemeKey) {
                setTheme(savedTheme);
            } else {
                const systemTheme = (systemColorScheme === lightThemeKey || systemColorScheme === darkThemeKey) 
                    ? systemColorScheme 
                    : lightThemeKey;
                setTheme(systemTheme)
            }
        } catch (error) {
            console.error('Failed to load theme:', error);
        }
    }

    const toggleTheme = async () => {
        const newTheme = theme === lightThemeKey ? darkThemeKey : lightThemeKey;
        setTheme(newTheme);

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