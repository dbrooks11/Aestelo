import {type JSX, useEffect, useState} from "react"
import { useTheme } from "../../context/ThemeContext";
import { ArrowLeft, Ellipsis } from "lucide-react"
import {motion, AnimatePresence} from 'framer-motion'
import { Moon, Sun} from "lucide-react";





export default function ProfileHeader(): JSX.Element{
    const {theme, toggleTheme} = useTheme()
    const [opaqueHeaderScroll, setOpaqueHeaderScroll] = useState<number>(0)

    useEffect(() => {
        const handleOpaqueHeader = () =>{
            const scrollY = window.scrollY
            const thresholdOpacity = 150

            const newOpacity = Math.min(scrollY / thresholdOpacity, 1)

            setOpaqueHeaderScroll(newOpacity)
        }

        window.addEventListener('scroll', handleOpaqueHeader)

        handleOpaqueHeader()

        return () => window.removeEventListener('scroll', handleOpaqueHeader)
    }, [])

    const headerStyle = {
        backgroundColor: `rgba(26, 26, 26, ${opaqueHeaderScroll})`, // 26,26,26 is approx charcoal/dark
        backdropFilter: `blur(${opaqueHeaderScroll * 10}px)` // Optional: adds nice blur as it darkens
    };
        

    function ThemeButton(): JSX.Element{
    return(
      <button className="flex justify-center items-center hover:bg-accents-primary/20 rounded-full w-10 h-10 text-white/75 transition-colors duration-300 hover:cursor-pointer bg-charcoal/50" onClick={toggleTheme}>
        <AnimatePresence mode="wait">
          <motion.div 
            key={theme}
            initial={{opacity: 0, rotate:-90 }}
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

    return(
        <header style={headerStyle} className='sticky z-20 top-0 text-black w-full h-16 flex justify-between items-center px-4'>
            <div>
                <button className="flex justify-center items-center hover:bg-accents-primary/20 rounded-full w-10 h-10 text-white/75 transition-colors duration-300 hover:cursor-pointer bg-charcoal/50"><ArrowLeft className="w-2/3 h-2/3"/></button>
            </div>
            <div className="flex gap-8">
                <ThemeButton/>
                <button className="flex justify-center items-center hover:bg-accents-primary/20 rounded-full w-10 h-10 text-white/75 transition-colors duration-300 hover:cursor-pointer bg-charcoal/50"><Ellipsis className="w-2/3 h-2/3"/></button>
            </div>
        </header>
    )
}