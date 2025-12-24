import {type JSX, type ReactElement, useEffect, useState} from "react"
import { Link, useNavigate } from "react-router-dom";
import { useTheme } from "../../context/ThemeContext";
import { ArrowLeft, Ellipsis, X, Settings, LogOut } from "lucide-react"
import { motion, useTransform, useScroll, AnimatePresence } from "framer-motion";
import { ThemeButton} from "../../hooks/ThemeProvider";
import type { AxiosResponse } from "axios";
import { protectedInstance, AxisErrorHelperConsoleOnly } from "../../util/axios_api_helpers";


type MenuLinks = {
    link: string
    className: string
    icon: ReactElement
    label: string
}

type ProfileHeaderProps = {
    username: string | undefined
    follower_count: number | undefined
}

type HeaderStyle = {
    backgroundColor: string
    backdropFilter: string
    borderBottom: string
}


const profileHeaderButtonStyle = "flex justify-center items-center hover:bg-accents-primary hover:dark:bg-accents-primary/35 rounded-full w-9 h-9 text-white/75 transition-colors duration-300 hover:cursor-pointer bg-charcoal/70"

const profileMenuLinksStyle = "flex items-center justify-center gap-2 p-2 border-b border-b-neutral-500/40"

const profileMenuIconsStyle = ""


const menuLinks: Array<MenuLinks> = [
    {
        link: "/",
        className: profileMenuLinksStyle,
        icon: <Settings className={profileMenuIconsStyle}/>,
        label: "Settings"
    },
    {
        link: "",
        className: profileHeaderButtonStyle,
        icon: <LogOut className="w-5"/>,
        label: "Logout"
    }
]

export default function ProfileHeader(props: ProfileHeaderProps): JSX.Element{
    
    const {scrollY} = useScroll()
    const {theme} = useTheme()
    const navigate = useNavigate()
    const [opaqueHeaderScroll, setOpaqueHeaderScroll] = useState<number>(0)
    const [isOpen, setIsOpen] = useState<boolean>(false)

    const toggleProfileMenu = () => {

        setIsOpen((prev: boolean): boolean => {
            return !prev ? true : false
        })
    }

    const handleMenuLinks = (): Array<JSX.Element> =>{

        const links: Array<JSX.Element> = menuLinks.map((items: MenuLinks)=>{
            if(items.link.includes('/logout') || (items.label.toLowerCase() == 'logout')){
                return(
                    <div className="flex justify-between md:justify-center">
                      <ThemeButton className={`${profileHeaderButtonStyle} flex md:hidden`}/>
                      <button title={items.label} onClick={logout} className={items.className}>{items.icon}</button>
                    </div>
                )
            }else{
            return(
                <Link to={items.link} className={items.className}>{items.icon}{items.label}</Link>
                )
            }
        })
        return links
    }

    async function logout(): Promise<void>{
      
        try{
          const response: AxiosResponse = await protectedInstance.post('/auth/logout')
    
          const data = response.data
    
          if(response.status === 200){
            console.log(data.message)
            navigate('/login-email')
          }
    
        }catch(error: unknown){
          AxisErrorHelperConsoleOnly(error, "Log Out")
        }
    
      }

    useEffect(() => {
        const handleOpaqueHeader = (): void =>{
            const scrollY: number = window.scrollY
            const thresholdOpacity: number = 150
            const maxOpacity: number = 0.60

            const newOpacity: number = Math.min((scrollY / thresholdOpacity), 1) * maxOpacity

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

    const headerStyle: HeaderStyle = {
        backgroundColor: theme === 'dark' ? `rgba(26, 26, 26, ${opaqueHeaderScroll})`: `rgba(250, 250, 248, ${opaqueHeaderScroll})` , 
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
                    <span className="dark:text-white/90 text-dark font-bold text-xs">{props.username}</span>
                    <span className="dark:text-neutral-400 text-neutral-500 text-[11px]">{props?.follower_count} Followers</span>
                </>: null}
                
            </motion.div>
            <div className="flex gap-4">
                <ThemeButton className={`${profileHeaderButtonStyle} hidden md:flex`}/>
                <button 
                  className={profileHeaderButtonStyle} 
                  onClick={toggleProfileMenu}
                  aria-label="Toggle Profile Menu"
                >{!isOpen ? <Ellipsis className="w-2/3 h-2/3"/>: <X className="w-2/3 h-2/3"/>}</button>
            </div>

            <AnimatePresence>
                {isOpen === true ? 
                    <motion.nav
                    key='Profile Menu'
                    initial={{opacity: 0}}
                    animate={{opacity: 1}}
                    exit={{opacity: 0}}
                    transition={{duration: 0.3, ease: "easeInOut"}}
                    className="absolute top-15 right-4 flex flex-col p-4 gap-2 bg-white/80 dark:bg-charcoal/80 backdrop-blur-lg rounded-br-sm rounded-tl-sm dark:text-white/95 text-sm border dark:border-neutral-800 border-neutral-300"
                    >
                        {handleMenuLinks()}
                    </motion.nav> : null}
            </AnimatePresence>
        </header>
    )
}