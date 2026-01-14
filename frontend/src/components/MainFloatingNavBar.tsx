import { useState, type ComponentType, type JSX, type SVGProps } from "react";
import { ChevronUp, House, Search, MapPinPlus, Map, User, Sun, Moon, type LucideProps } from "lucide-react";
import { Link, useLocation } from "react-router-dom";
import { AnimatePresence, motion, type Variants } from "framer-motion";
import cn from "../util/tailwind_merger";
import { useTheme } from "../context/ThemeContext";;

type IconComponent = ComponentType<LucideProps | SVGProps<SVGSVGElement>>

type NavButtonsType = {
    order: number
    label: string
    icon: IconComponent
    action?: () => void
    linkTo?: string
    className?: string 
}

const containerVariants: Variants = {
    hidden: { 
        opacity: 0, 
        y: 60, 
        scale: 0.3, 
        transition: { 
            type: "spring",
            stiffness: 400,
            damping: 20,
            when: "afterChildren", 
            staggerChildren: 0.04,
            staggerDirection: -1 
        }
    },
    visible: { 
        opacity: 1, 
        y: 0, 
        scale: 1,
        transition: { 
            type: "spring", 
            stiffness: 300, 
            damping: 20,
            staggerChildren: 0.05, 
            delayChildren: 0.1,
            staggerDirection: -1
        }
    }
};

const itemVariants: Variants = {
    hidden: { opacity: 0, y: 20, scale: 0.5 },
    visible: { opacity: 1, y: 0, scale: 1 }
};

export default function MainFloatingNavBar({openModal}: {openModal: () => void}): JSX.Element {
    const {theme, toggleTheme} = useTheme()
    const location = useLocation()
    const [isNavOpen, setIsNavOpen] = useState<boolean>(false)


    const navButtons: Array<NavButtonsType> = [
        {
            order: 1,
            label: 'Change Theme',
            icon: theme === 'light' ? Sun : Moon,
            action: toggleTheme
        },
        {
            order: 2,
            label: 'Map',
            icon: Map, 
            linkTo: '/map', 
        },
        {
            order: 3,
            label: 'Search',
            icon: Search,
            linkTo: '/explore',
        },
        {
            order: 4,
            label: 'Spot',
            icon: MapPinPlus,
            action: openModal
        },
        {
            order: 5,
            label: 'Feed',
            icon: House,
            linkTo: '/post/feed',
        },
        {
            order: 6,
            label: 'Profile',
            icon: User,
            linkTo: '/profile/me',
        }
    ]   

    const handleNavButtonLinks = (): JSX.Element => {
        const orderLinks = navButtons.sort((nav1, nav2) => nav1.order - nav2.order)

        return (
            <>
                {orderLinks.map((nav) => {
                    const isActive = location.pathname === nav.linkTo

                    return (
                        <motion.div
                            key={nav.order}
                            variants={itemVariants}
                            className={` group relative`} 
                        >
                            {/* Tooltip Label (Left side) */}
                            <div 
                                aria-hidden="true"
                                className="top-1/2 right-full absolute bg-white dark:bg-neutral-900 opacity-0 group-hover:opacity-100 shadow-lg mr-3 px-2 py-1 border border-gray-100 dark:border-white/10 rounded font-bold text-black dark:text-white text-xs whitespace-nowrap transition-opacity -translate-y-1/2 pointer-events-none">
                                {nav.label}
                                {/* Tiny arrow pointing right */}
                                <div className="top-1/2 -right-1 absolute bg-white dark:bg-neutral-900 border-gray-100 dark:border-white/10 border-t border-r w-2 h-2 rotate-45 -translate-y-1/2"></div>
                            </div>
                            {/* TODO: fix theme button in menu */}

                            {nav.action !== undefined ? 
                            <button
                                title={nav.label}
                                aria-label={nav.label}
                                aria-current={isActive ? 'page' : undefined}
                                className={cn(
                                    "flex justify-center items-center rounded-full w-12 h-12 group-hover:scale-110 transition-all duration-200 cursor-pointer",
                                    isActive 
                                        ? "bg-accents-deep text-white shadow-[0_0_10px_rgba(200,90,94,0.5)]" 
                                        : "text-gray-500 hover:text-black hover:bg-gray-100 dark:text-gray-400 dark:hover:text-white dark:hover:bg-white/10",
                                    nav.className
                                )}
                                onClick={() => {
                                    if(nav.action !== undefined) nav.action()
                                }} 
                            >
                                <nav.icon className="w-6 h-6"></nav.icon>
                            </button> :
                            <Link
                                to={nav.linkTo ? nav.linkTo : ''}
                                title={nav.label}
                                aria-label={nav.label}
                                aria-current={isActive ? 'page' : undefined}
                                className={cn(
                                    "flex justify-center items-center rounded-full w-12 h-12 group-hover:scale-110 transition-all duration-200",
                                    isActive 
                                        ? "bg-accents-deep text-white shadow-[0_0_10px_rgba(200,90,94,0.5)]" 
                                        : "text-gray-500 hover:text-black hover:bg-gray-100 dark:text-gray-400 dark:hover:text-white dark:hover:bg-white/10",
                                    nav.className
                                )}
                            >
                                <nav.icon></nav.icon>
                            </Link>}
                        </motion.div>
                    )
                })}
            </>
        )
    }

    return (
        <div className="right-6 bottom-6 z-50 fixed flex flex-col items-center gap-4"> 
            
            <AnimatePresence>
                {isNavOpen && (
                    <motion.nav
                        id="main-floating-nav"
                        aria-label="Main Navigation"
                        variants={containerVariants}
                        initial="hidden"
                        animate="visible"
                        exit="hidden"
                        className="bottom-0 z-0 absolute flex flex-col items-center gap-3 bg-white/90 dark:bg-neutral-900/90 shadow-2xl backdrop-blur-xl p-2 pb-20 border border-gray-200 dark:border-white/10 rounded-full origin-bottom"
                        style={{ paddingBottom: "5rem" }}
                    >
                        {handleNavButtonLinks()}
                    </motion.nav>
                )}
            </AnimatePresence>

            {/* Main Toggle Button */}
            <motion.button
                type="button"
                aria-label={isNavOpen ? "Close menu" : "Open menu"}
                aria-expanded={isNavOpen}
                aria-controls="main-floating-nav"
                className="z-10 flex justify-center items-center bg-accents-primary/95 shadow-[0_4px_10px_rgba(200,90,94,0.5)] hover:shadow-[0_6px_20px_rgba(200,90,94,0.7)] mb-1 rounded-full w-14 h-14 text-white transition-shadow cursor-pointer"
                onClick={() => setIsNavOpen(!isNavOpen)}
                whileTap={{ scale: 0.9 }}
                animate={{ rotate: isNavOpen ? 180 : 0 }} 
            >
                <ChevronUp size={30} aria-hidden="true" />
            </motion.button>
        </div>
    )
}