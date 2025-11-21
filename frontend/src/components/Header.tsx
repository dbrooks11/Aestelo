// Universal Header
import { type JSX, type Dispatch, type SetStateAction} from "react";
import {motion, AnimatePresence} from 'framer-motion'
import { Moon, Sun, Search, Menu } from "lucide-react";
import { Link, useNavigate, type NavigateFunction, useLocation} from "react-router-dom";
import {AxisErrorHelperConsoleOnly, protectedInstance } from "../util/axios_api_helpers";
import type { AxiosResponse } from "axios";


type HeaderProps = {
  theme: 'light' | 'dark'
  setTheme: Dispatch<SetStateAction<'light' | 'dark'>>
  isAuthenticated: boolean
}


export default function Header({isAuthenticated, setTheme, theme}: HeaderProps): JSX.Element {

  const navigate: NavigateFunction = useNavigate()
  const location = useLocation()

  const hideSearchPaths: Array<string> = ['/profile/me']

  function setThemeHeader():void{
        setTheme((prevTheme: HeaderProps['theme'])=>{
          const newTheme: HeaderProps['theme'] = prevTheme === 'light' ? 'dark' : 'light'
          return newTheme
        })
  }


  async function logout(): Promise<void>{
  
    try{
      const response: AxiosResponse = await protectedInstance.post('auth/logout')

      const data = response.data

      if(response.status === 200){
        console.log(data.message)
        navigate('/login-email')
      }

    }catch(error: unknown){
      AxisErrorHelperConsoleOnly(error, "Log Out")
    }

  }

  function loginRouting(): void{
    navigate('/login-email')
  }

  function signupRouting(): void{
    navigate('/signup')
  }


  function ThemeButton(): JSX.Element{
    return(
      <button className="theme_button" onClick={setThemeHeader}>
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
    <header className="header_container">
        {/* Header Links */}
        {!isAuthenticated ? <nav className=" hidden md:flex gap-8 dark:text-mid-gray text-black/75 text-sm p-1 min-w-1/3">
          <Link className="header_links" to="/">Home</Link>
          <Link className="header_links" to="/about">About</Link>
          <Link className="header_links" to="/explore">Explore</Link>
        </nav>: null}

        {/* Aestelo Logo */}
        <div className={`${isAuthenticated ? 'w-1/3 min-w-fit' : null}`}>
          <span className="text-3xl text-black dark:text-white">Aeste<span className="text-accents-primary">lo</span></span>
        </div>

          {/* Dropdown menu for smaller screens */}
        {!isAuthenticated ? 
        <div className="flex gap-6 md:hidden">
          <ThemeButton/>
          <button type="button" className="text-accents-primary cursor-pointer w-8 hover:text-accents-deep ">
            <nav>
              <Menu className="w-full h-full"/>
            </nav>
        </button>
        </div>: null}

        {/* Search Input for Authenticated Users */}
        {isAuthenticated && !hideSearchPaths.includes(location.pathname) ? <form className="w-1/3">
          <label htmlFor="search" className="text-sm font-medium text-gray-900 sr-only dark:text-white">Search</label>
          <div className="relative">
            <div className="absolute inset-y-0 start-0 flex items-center pl-3">
                <Search className="w-5 text-black dark:text-white"/>
            </div>
            <input type="search" id="search" className="block w-full pl-9 py-1.5 pr-2 bg-bg-light border-2 border-neutral-300 hover:border-neutral-400/60 dark:border-stone-600/60 dark:hover:border-stone-600/90 dark:bg-smoke/60 text-heading text-sm rounded-xl focus:outline-none dark:focus:border-accents-deep focus:border-accents-primary shadow-xs placeholder:text-body hover:cursor-pointer focus:cursor-text" placeholder="Search" required />
          </div>
        </form>: null}

        {/* Regular Header for Public users */}
        {!isAuthenticated ? <div className="hidden md:flex gap-4 text-white justify-end min-w-1/3 xs:max-md:hidden">
            <ThemeButton/>
            <button className="header_login_button" onClick={loginRouting}>Login</button>
            <button className="header_signup_button" onClick={signupRouting}>SignUp</button>
        </div>: null}

        {/* Header for Authenticated Users */}
        {isAuthenticated ? <nav className={`flex gap-8 items-center ${!hideSearchPaths.includes(location.pathname) ? 'w-1/3 min-w-fit justify-end' : null}`}>
            <Link to="/profile/me">Profile</Link>
            <Link to="/post/feed">Feed</Link>
            <div className="flex items-center border-l pl-3 gap-3">
              <ThemeButton/>
              <button className="header_logout_button" onClick={logout}>Logout</button>
            </div>
        </nav>: null}
    </header>
  )
}
