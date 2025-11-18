// Universal Header
import { type JSX, type Dispatch, type SetStateAction} from "react";
import {motion, AnimatePresence} from 'framer-motion'
import { Moon, Sun } from "lucide-react";
import { Search } from 'lucide-react';
import { Link, useNavigate, type NavigateFunction } from "react-router-dom";
import {AxisErrorHelperConsoleOnly, protectedInstance } from "../util/axios_api_helpers";
import type { AxiosResponse } from "axios";


type HeaderProps = {
  theme: 'light' | 'dark'
  setTheme: Dispatch<SetStateAction<'light' | 'dark'>>
  isAuthenticated: boolean
}


export default function Header({isAuthenticated, setTheme, theme}: HeaderProps): JSX.Element {

  const navigate: NavigateFunction = useNavigate()


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
        {!isAuthenticated ? <nav className="flex gap-8 dark:text-mid-gray text-black/75 text-sm p-1 min-w-1/3">
          <Link className="header_links" to="/">Home</Link>
          <Link className="header_links" to="/about">About</Link>
          <Link className="header_links" to="/explore">Explore</Link>
        </nav>: null}

        {/* Aestelo Logo */}
        <div>
          <span className="text-3xl text-black dark:text-white">Aeste<span className="text-accents-primary">lo</span></span>
        </div>

        {/* Search Input for Authenticated Users */}
        {isAuthenticated ? <form>
          <Search/>
          <input className="border border-black rounded-lg" type="search" id="search" name="search"></input>
        </form>: null}

        {/* Regular Header for Public users */}
        {!isAuthenticated ? <div className="flex gap-4 text-white justify-end min-w-1/3">
            <ThemeButton/>
            <button className="header_login_button" onClick={loginRouting}>Login</button>
            <button className="header_signup_button" onClick={signupRouting}>SignUp</button>
        </div>: null}

        {/* Header for Authenticated Users */}
        {isAuthenticated ? <nav className="flex gap-8 items-center">
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
