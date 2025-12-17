// Universal Header
import { type JSX, type Dispatch, type SetStateAction, useState} from "react";
import { useAuth } from "../../context/AuthContext";
import {motion, AnimatePresence} from 'framer-motion'
import { Moon, Sun, Menu } from "lucide-react";
import { Link, useNavigate, type NavigateFunction} from "react-router-dom";



type HeaderProps = {
  theme: 'light' | 'dark'
  setTheme: Dispatch<SetStateAction<'light' | 'dark'>>
}


export default function Header({ setTheme, theme}: HeaderProps): JSX.Element {

  const {isAuthenticated} = useAuth()
  const [isDropwdown, setIsDropwdown] = useState<boolean>(false)
  const navigate: NavigateFunction = useNavigate()

  function setThemeHeader():void{
        setTheme((prevTheme: HeaderProps['theme'])=>{
          const newTheme: HeaderProps['theme'] = prevTheme === 'light' ? 'dark' : 'light'
          return newTheme
        })
  }

  function loginRouting(): void{
    if(isAuthenticated){
      navigate('/profile/me')
    }else{
      navigate('/login-email')
    }
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

  function toggleDropdown(){
    setIsDropwdown((bool)=>{
      return bool ? false : true
    })
  }

  
  return (
    // todo: remove home links for production(home link will be logo)
    <header className="header_container">
        {/* Header Links */}
        <nav className=" hidden md:flex gap-8 dark:text-mid-gray text-black/75 text-sm p-1 min-w-1/3">
          <Link className="header_links" to="/">Home</Link>
          <Link className="header_links" to="/about">About</Link>
          <Link className="header_links" to="/explore">Explore</Link>
        </nav>

        {/* Aestelo Logo */}
        <div>
          <span className="text-3xl text-black dark:text-white">Aeste<span className="text-accents-primary">lo</span></span>
        </div>

          {/* Dropdown Menu for smaller screens */}
        {!isAuthenticated ? 
        <div className="flex gap-6 md:hidden">
          <ThemeButton/>
          <button onClick={toggleDropdown} type="button" className="text-accents-primary cursor-pointer w-8 hover:text-accents-deep ">
              <Menu className="w-full h-full"/>
        </button>
        {isDropwdown ? <nav id="nav-dropdown-menu" className="">
          <ul>
            <li>
              <Link className="header_links" to="/">Home</Link>
            </li>
            <li>
              <Link className="header_links" to="/about">About</Link>
            </li>
            <li>
              <Link className="header_links" to="/explore">Explore</Link>
            </li>
          </ul>
        </nav>: null}
        </div>: null}

        {/* Regular Header for Public users */}
        <div className="hidden md:flex gap-4 text-white justify-end min-w-1/3 xs:max-md:hidden">
            <ThemeButton/>
            <button className="header_login_button" onClick={loginRouting}>Login</button>
            <button className="header_signup_button" onClick={signupRouting}>SignUp</button>
        </div>
    </header>
  )
}
