import {type JSX, useEffect, useState} from "react"
import { useTheme } from "../../context/ThemeContext";
import { ArrowLeft, Ellipsis } from "lucide-react"
import { motion, useTransform, useScroll } from "framer-motion";
import { ThemeButton } from "../../hooks/ThemeProvider";


const profileHeaderButtonStyle = "flex justify-center items-center hover:bg-accents-primary hover:dark:bg-accents-primary/35 rounded-full w-9 h-9 text-white/75 transition-colors duration-300 hover:cursor-pointer bg-charcoal/70"


type ProfileHeaderProps = {
    username: string | undefined
    follower_count: number | undefined
}

export default function ProfileHeader(props: ProfileHeaderProps): JSX.Element{
    
    const {scrollY} = useScroll()
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
        backdropFilter: `blur(${opaqueHeaderScroll * 35}px)` ,
        borderBottom: `${opaqueHeaderScroll > .55 ? `1px solid ${theme === 'dark' ? 'oklch(26.9% 0 0)' : 'oklch(90% 0 0)'}` : 'none'}`
    };
        

    return(
        <header style={headerStyle} className='sticky z-50 top-0 w-full h-16 flex justify-between items-center px-4'>
            <div>
                <button className={profileHeaderButtonStyle}><ArrowLeft className="w-2/3 h-2/3"/></button>
            </div>
            <motion.div 
            className="text-black flex flex-col items-center justify-center"
            style={{y: useTransform(scrollY, [100, 200], [50, 0]), opacity: useTransform(scrollY, [160, 200], [0, 1])}}
            >
                {opaqueHeaderScroll > .55 ? <>
                    <span className="dark:text-white/90 text-dark font-bold text-sm">{props.username}</span>
                    <span className="dark:text-neutral-400 text-neutral-500 text-xs">{props?.follower_count} Followers</span>
                </>: null}
                
            </motion.div>
            <div className="flex gap-4">
                <ThemeButton className={profileHeaderButtonStyle}/>
                <button className={profileHeaderButtonStyle}><Ellipsis className="w-2/3 h-2/3"/></button>
            </div>
        </header>
    )
}