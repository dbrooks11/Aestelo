import {type JSX, type ReactElement, useEffect, useState} from "react"
import { Link, useNavigate } from "react-router-dom";
import { useTheme } from "../../context/ThemeContext";
import { ArrowLeft, Ellipsis, X, Settings, LogOut } from "lucide-react"
import { motion, useTransform, useScroll, AnimatePresence } from "framer-motion";
import { ThemeButton} from "../../hooks/ThemeProvider";
import { type ProfileDataType  } from "../../pages/ProfilePage";
import type { AxiosResponse } from "axios";
import { protectedInstance, AxisErrorHelperConsoleOnly } from "../../util/axios_api_helpers";
import toast from "react-hot-toast";


type MenuLinks = {
    link: string
    className: string
    icon: ReactElement
    label: string
}

type ProfileHeaderProps = {
    username: ProfileDataType['username']
    follower_count: ProfileDataType['follower_count']
}

type HeaderStyle = {
    backgroundColor: string
    backdropFilter: string
    borderBottom: string
}


const profileHeaderButtonStyle = "flex justify-center items-center hover:bg-accents-primary hover:dark:bg-accents-deep/40 rounded-full w-9 h-9 text-white/75 transition-colors duration-300 hover:cursor-pointer bg-charcoal/70"

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
                    <div className="flex justify-between md:justify-center" key={items.label}>
                      <ThemeButton className={`${profileHeaderButtonStyle} flex md:hidden`}/>
                      <button title={items.label} onClick={logout} className={items.className}>{items.icon}</button>
                    </div>
                )
            }else{
            return(
                <Link to={items.link} className={items.className} key={items.label}>{items.icon}{items.label}</Link>
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
            navigate('/login-email')
            toast.success(data.message, {
                toasterId: 'login'
            })
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
        <header 
            style={headerStyle} 
            className='top-0 z-50 sticky flex justify-between items-center px-4 w-full h-16'
        >
            
            {/* Go back button */}
            <div>
                <button 
                    className={profileHeaderButtonStyle} 
                    aria-label="Go back"
                    onClick={()=> navigate(-1)} //TODO: fix to only go back to neccesary pages
                >
                    <ArrowLeft className="w-2/3 h-2/3" aria-hidden="true"/>
                </button>
            </div>

            {/* Dynamic Title */}
            <motion.div 
                className="flex flex-col justify-center items-center text-black"
                style={{
                    y: useTransform(scrollY, [100, 200], [50, 0]), 
                    opacity: useTransform(scrollY, [160, 200], [0, 1])
                }}
                aria-hidden={opaqueHeaderScroll <= 0.55} 
            >
                {opaqueHeaderScroll > .55 ? (
                    <>
                        <span className="font-bold text-dark dark:text-white/90 text-xs">
                            {props.username}
                        </span>
                        <span className="text-[11px] text-neutral-500 dark:text-neutral-400">
                            {props?.follower_count} Followers
                        </span>
                    </>
                ) : null}
            </motion.div>

            {/* Hamburger menu */}
            <div className="flex gap-4">
                {/* Theme Toggle (Hidden on mobile) */}
                <div className="hidden md:flex">
                    <ThemeButton className={profileHeaderButtonStyle} />
                </div>

                {/* Profile Menu Toggle */}
                <button 
                    className={profileHeaderButtonStyle} 
                    onClick={toggleProfileMenu}
                    aria-label={isOpen ? "Close Profile Menu" : "Open Profile Menu"}
                    aria-expanded={isOpen} 
                    aria-haspopup="true"   
                >
                    {!isOpen ? (
                        <Ellipsis className="w-2/3 h-2/3" aria-hidden="true"/>
                    ) : (
                        <X className="w-2/3 h-2/3" aria-hidden="true"/>
                    )}
                </button>
            </div>

            {/* Dropdown menu */}
            <AnimatePresence>
                {isOpen === true ? (
                    <motion.nav
                        key='Profile Menu'
                        initial={{opacity: 0}}
                        animate={{opacity: 1}}
                        exit={{opacity: 0}}
                        transition={{duration: 0.3, ease: "easeInOut"}}
                        className="top-15 right-4 absolute flex flex-col gap-2 bg-white/80 dark:bg-charcoal/80 backdrop-blur-lg p-4 border border-neutral-300 dark:border-neutral-800 rounded-tl-sm rounded-br-sm dark:text-white/95 text-sm"
                        aria-label="Profile Options"
                    >
                        {handleMenuLinks()}
                    </motion.nav> 
                ) : null}
            </AnimatePresence>
        </header>
    )
}