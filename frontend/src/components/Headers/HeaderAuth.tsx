// Universal Header
import { type JSX } from "react";
import { type HeaderProps } from "../../hooks/AuthProvider";
import { useTheme } from "../../context/ThemeContext";
import {motion, AnimatePresence} from 'framer-motion'
import { Moon, Sun, Search} from "lucide-react";
import { Link, useNavigate, type NavigateFunction, useLocation} from "react-router-dom";
import {AxisErrorHelperConsoleOnly, protectedInstance } from "../../util/axios_api_helpers";
import type { AxiosResponse } from "axios";



export default function ProtectedHeader({ setTheme, theme}: HeaderProps): JSX.Element {
  const navigate: NavigateFunction = useNavigate()
  const location = useLocation()

  const {toggleTheme} = useTheme()

  const hideSearchPaths: Array<string> = ['/profile/me']

  


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

  function ThemeButton(): JSX.Element{
    return(
      <button className="theme_button" onClick={toggleTheme}>
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


  return (
    // todo: remove home links for production(home link will be logo)
    <header className= 'bg-bg-light-secondary/50 dark:bg-charcoal/65 backdrop-blur-lg top-0 z-50 sticky flex items-center justify-between px-12 py-3 border-b-neutral-200 dark:border-b-black font-semibold dark:text-bg-light-secondary'>

        {/* Aestelo Logo */}
        <div className='w-1/3 min-w-fit'>
          <span className="text-3xl text-black dark:text-white">Aeste<span className="text-accents-primary">lo</span></span>
        </div>

        {/* Search Input for Authenticated Users */}
        {!hideSearchPaths.includes(location.pathname) ? <form className="w-1/3">
          <label htmlFor="search" className="text-sm font-medium text-gray-900 sr-only dark:text-white">Search</label>
          <div className="relative">
            <div className="absolute inset-y-0 start-0 flex items-center pl-3">
                <Search className="w-5 text-black dark:text-white"/>
            </div>
            <input type="search" id="search" className="block w-full pl-9 py-1.5 pr-2 bg-bg-light border-2 border-neutral-300 hover:border-neutral-400/60 dark:border-stone-600/60 dark:hover:border-stone-600/90 dark:bg-smoke/60 text-heading text-sm rounded-xl focus:outline-none dark:focus:border-accents-deep focus:border-accents-primary shadow-xs placeholder:text-body hover:cursor-pointer focus:cursor-text" placeholder="Search" required />
          </div>
        </form>: null}

        {/* Header for Authenticated Users */}
        <nav className={`flex gap-8 items-center ${!hideSearchPaths.includes(location.pathname) ? 'w-1/3 min-w-fit justify-end' : null}`}>
            <Link to="/profile/me">Profile</Link>
            <Link to="/post/feed">Feed</Link>
            <div className="flex items-center border-l pl-3 gap-3">
              <ThemeButton/>
              <button className="header_logout_button" onClick={logout}>Logout</button>
            </div>
        </nav>
    </header>
  )
}
