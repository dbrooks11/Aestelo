import {type JSX, useEffect, useState} from "react"
import { useTheme } from "../../context/ThemeContext";
import { ArrowLeft, Ellipsis } from "lucide-react"
import { ThemeButton } from "../../hooks/ThemeProvider";


export default function ProfileHeader(): JSX.Element{
    
    const {theme} = useTheme()
    const [opaqueHeaderScroll, setOpaqueHeaderScroll] = useState<number>(0)

    useEffect(() => {
        const handleOpaqueHeader = () =>{
            const scrollY = window.scrollY
            const thresholdOpacity = 150
            const maxOpacity = 0.60

            const newOpacity = Math.min((scrollY / thresholdOpacity), 1) * maxOpacity

            setOpaqueHeaderScroll((prev: number)=>{
                if(newOpacity === maxOpacity && prev === maxOpacity) return prev
                if(newOpacity === 0 && prev === 0) return prev
                return newOpacity
            })
        }

        window.addEventListener('scroll', handleOpaqueHeader)

        handleOpaqueHeader()

        return () => window.removeEventListener('scroll', handleOpaqueHeader)
    }, [])

    const headerStyle = {
        backgroundColor: theme === 'dark' ? `rgba(26, 26, 26, ${opaqueHeaderScroll})`: `rgba(255, 255, 255, ${opaqueHeaderScroll})` , 
        backdropFilter: `blur(${opaqueHeaderScroll * 50}px)` 
    };

    
        

    return(
        <header style={headerStyle} className='sticky z-50 top-0 w-full h-16 flex justify-between items-center px-4'>
            <div>
                <button className="flex justify-center items-center hover:bg-accents-primary hover:dark:bg-accents-primary/20 rounded-full w-10 h-10 text-white/75 transition-colors duration-300 hover:cursor-pointer bg-charcoal/50"><ArrowLeft className="w-2/3 h-2/3"/></button>
            </div>
            <div className="flex gap-6">
                <ThemeButton className="flex justify-center items-center hover:bg-accents-primary/20 rounded-full w-10 h-10 text-white/75 transition-colors duration-300 hover:cursor-pointer bg-charcoal/50"/>
                <button className="flex justify-center items-center hover:bg-accents-primary hover:dark:bg-accents-primary/20 rounded-full w-10 h-10 text-white/75 transition-colors duration-300 hover:cursor-pointer bg-charcoal/50"><Ellipsis className="w-2/3 h-2/3"/></button>
            </div>
        </header>
    )
}