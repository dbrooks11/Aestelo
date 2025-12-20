import { useState, useEffect, type ReactNode } from "react";
import { type ThemeContextType, type Theme,ThemeContext } from "../context/ThemeContext";



export default function ThemeProvider({ children }: {children: ReactNode}){

    const [theme, setTheme] = useState<'light' | 'dark'>(() => (localStorage.getItem("theme") as Theme) ?? "light")
      
    useEffect(() => {
        localStorage.setItem('theme', theme)
    }, [theme]);

    function toggleTheme():void{
        setTheme((prevTheme: ThemeContextType['theme'])=>{
          const newTheme: ThemeContextType['theme'] = prevTheme === 'light' ? 'dark' : 'light'
          return newTheme
        })
  }


    return(
        <ThemeContext.Provider value={{theme, setTheme, toggleTheme}}>
            {children}
        </ThemeContext.Provider>
    )

}