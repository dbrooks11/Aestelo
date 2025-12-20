import { type Dispatch, type SetStateAction, createContext, useContext } from "react";


export type Theme = 'light' | 'dark'

export type ThemeContextType = {
  theme: Theme
  setTheme: Dispatch<SetStateAction<Theme>>
  toggleTheme: () => void;
}

export const ThemeContext = createContext<ThemeContextType | undefined>(undefined)

export const useTheme = () =>{
    const context = useContext(ThemeContext)
    if(!context){
        throw new Error("useTheme must be used within a ThemeProvider")
    }
    return context
}