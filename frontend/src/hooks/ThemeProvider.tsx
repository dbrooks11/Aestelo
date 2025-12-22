import { useState, useEffect, type ReactNode, type JSX } from "react";
import { useTheme } from "../context/ThemeContext";
import cn from "../util/tailwind_merger";
import { type ThemeContextType, type Theme,ThemeContext } from "../context/ThemeContext";
import { AnimatePresence, motion } from "framer-motion";
import { Moon, Sun } from "lucide-react";


export function ThemeButton({className = ""}: {className: string}): JSX.Element{
    const {theme, toggleTheme} = useTheme()

    return(
      <button onClick={toggleTheme} className={cn('', className)}>
        <AnimatePresence mode="wait">
          <motion.div 
            key={theme}
            initial={{opacity: 0, rotate: -90 }}
            animate={{opacity: 1, rotate: 0}}
            exit={{opacity: 0, rotate: 90}}
            transition={{duration: 0.2}}
            >
            {theme === 'light' ? <Moon size={20}/> : <Sun size={20}/>}
            </motion.div>
        </AnimatePresence>
      </button>
    )
  }

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
        <ThemeContext.Provider value={{theme, setTheme, toggleTheme,}}>
            {children}
        </ThemeContext.Provider>
    )

}