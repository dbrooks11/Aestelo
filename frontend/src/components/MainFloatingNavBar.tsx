import { useState, type JSX, type ReactElement } from "react";
import { ChevronUp, House, Search, SquarePlus, Map, User } from "lucide-react";
import { Link, useLocation } from "react-router-dom";
import { AnimatePresence, motion, type Variants } from "framer-motion";
import cn from "../util/tailwind_merger";
import { ThemeButton } from "../hooks/ThemeProvider";

type NavButtonsType = {
    order: number
    label: string
    icon: ReactElement
    linkTo: string
    className?: string // Optional
}

const navButtons: Array<NavButtonsType> = [
    {
        order: 1,
        label: 'Change Theme',
        icon: <ThemeButton className=""/>,
        linkTo: ''
    },
    {
        order: 2,
        label: 'Map',
        icon: <Map className="w-6 h-6" />, 
        linkTo: '/map', 
    },
    {
        order: 3,
        label: 'Search',
        icon: <Search className="w-6 h-6" />,
        linkTo: '/explore',
    },
    {
        order: 4,
        label: 'Post',
        icon: <SquarePlus className="w-6 h-6" />,
        linkTo: '/create',
    },
    {
        order: 5,
        label: 'Feed',
        icon: <House className="w-6 h-6" />,
        linkTo: '/post/feed',
    },
    {
        order: 6,
        label: 'Profile',
        icon: <User className="w-6 h-6" />,
        linkTo: '/profile/me',
    }
]

const containerVariants: Variants = {
    hidden: { 
        opacity: 0, 
        y: 60, 
        scale: 0.3, 
        transition: { 
            type: "spring",
            stiffness: 400,
            damping: 30,
            when: "afterChildren", 
            staggerChildren: 0.05,
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
            staggerChildren: 0.07, 
            delayChildren: 0.1,
            staggerDirection: -1
        }
    }
};

const itemVariants: Variants = {
    hidden: { opacity: 0, y: 20, scale: 0.5 },
    visible: { opacity: 1, y: 0, scale: 1 }
};

export default function MainFloatingNavBar(): JSX.Element {
    const location = useLocation()
    const [isNavOpen, setIsNavOpen] = useState<boolean>(false)

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
                            className="relative group" 
                        >
                            {/* Tooltip Label (Left side) */}
                            <div className="absolute right-full top-1/2 -translate-y-1/2 mr-3 px-2 py-1 rounded bg-neutral-900 text-white text-xs font-bold whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none shadow-lg">
                                {nav.label}
                                {/* Tiny arrow pointing right */}
                                <div className="absolute top-1/2 -right-1 -translate-y-1/2 w-2 h-2 bg-neutral-900 rotate-45"></div>
                            </div>

                            {nav.label.toLowerCase().includes('theme') && nav.icon}

                            {!nav.label.toLowerCase().includes('theme') && <Link
                                to={nav.linkTo}
                                title={nav.label}
                                className={cn(
                                    "flex items-center justify-center w-12 h-12 rounded-full transition-all duration-200 group-hover:scale-110",
                                    isActive 
                                        ? "bg-accents-deep text-white shadow-[0_0_10px_rgba(244,63,94,0.5)]" 
                                        : "text-neutral-400 hover:text-white hover:bg-white/10",
                                    nav.className
                                )}
                                onClick={() => setIsNavOpen(false)} 
                            >
                                {nav.icon}
                            </Link>}
                        </motion.div>
                    )
                })}
            </>
        )
    }

    return (
        <div className="flex flex-col items-center fixed right-6 bottom-6 z-50 gap-4"> 
            
            <AnimatePresence>
                {isNavOpen && (
                    <motion.nav
                        variants={containerVariants}
                        initial="hidden"
                        animate="visible"
                        exit="hidden"
                        className="absolute bottom-0 z-0 flex flex-col items-center gap-3 p-2 pb-20 rounded-full bg-neutral-900/90 dark:bg-neutral-800/90 backdrop-blur-xl border border-white/10 shadow-2xl origin-bottom"
                        style={{ paddingBottom: "5rem" }}
                    >
                        {handleNavButtonLinks()}
                    </motion.nav>
                )}
            </AnimatePresence>

            {/* Main Toggle Button */}
            <motion.button
                className="w-14 h-14 mb-1 rounded-full bg-accents-primary/95 text-white shadow-[0_4px_10px_rgba(200,90,94,0.5)] flex items-center justify-center z-10 hover:shadow-[0_6px_20px_rgba(200,90,94,0.7)] transition-shadow cursor-pointer"
                onClick={() => setIsNavOpen(!isNavOpen)}
                whileTap={{ scale: 0.9 }}
                animate={{ rotate: isNavOpen ? 180 : 0 }} 
            >
                <ChevronUp size={30} />
            </motion.button>
        </div>
    )
}