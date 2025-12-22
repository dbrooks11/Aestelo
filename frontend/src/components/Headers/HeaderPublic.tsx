// Universal Header
import { type JSX, useState} from "react";
import { type HeaderProps } from "../../hooks/AuthProvider";
import { useAuth } from "../../context/AuthContext";
import { ThemeButton } from "../../hooks/ThemeProvider";
import { Link, useNavigate, type NavigateFunction} from "react-router-dom";
import { head } from "framer-motion/client";
import { Menu } from "lucide-react";


const headerLinksStyle = "transition hover:scale-110 dark:hover:text-bg-light hover:text-black cursor-pointer"

export default function PublicHeader({ setTheme, theme}: HeaderProps): JSX.Element {

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


  function toggleDropdown(){
    setIsDropwdown((bool)=>{
      return bool ? false : true
    })
  }

  
  return (
    // todo: remove home links for production(home link will be logo)
    <header className='top-0 z-50 sticky flex items-center justify-between px-12 py-3 border-b-neutral-200 dark:border-b-black font-semibold dark:text-bg-light-secondary bg-bg-light-secondary/50 dark:bg-charcoal/65 backdrop-blur-lg ' >
        {/* Header Links */}
        <nav className=" hidden md:flex gap-8 dark:text-mid-gray text-black/75 text-sm p-1 min-w-1/3">
          <Link className={headerLinksStyle} to="/">Home</Link>
          <Link className={headerLinksStyle} to="/about">About</Link>
          <Link className={headerLinksStyle} to="/explore">Explore</Link>
        </nav>

        {/* Aestelo Logo */}
        <div>
          <span className="text-3xl text-black dark:text-white">Aeste<span className="text-accents-primary">lo</span></span>
        </div>

          {/* Dropdown Menu for smaller screens */}
        {!isAuthenticated ? 
        <div className="flex gap-6 md:hidden">
          <ThemeButton className="flex justify-center items-center hover:bg-accents-primary/20 rounded-full w-10 h-10 text-black dark:text-white transition-colors duration-300 hover:cursor-pointer"/>
          <button onClick={toggleDropdown} type="button" className="text-accents-primary cursor-pointer w-8 hover:text-accents-deep ">
              <Menu className="w-full h-full"/>
        </button>
        {isDropwdown ? <nav id="nav-dropdown-menu" className="">
          <ul>
            <li>
              <Link className={headerLinksStyle} to="/">Home</Link>
            </li>
            <li>
              <Link className={headerLinksStyle} to="/about">About</Link>
            </li>
            <li>
              <Link className={headerLinksStyle} to="/explore">Explore</Link>
            </li>
          </ul>
        </nav>: null}
        </div>: null}

        {/* Regular Header for Public users */}
        <div className="hidden md:flex gap-4 text-white justify-end min-w-1/3 xs:max-md:hidden">
            <ThemeButton className="flex justify-center items-center hover:bg-accents-primary/20 rounded-full w-10 h-10 text-black dark:text-white transition-colors duration-300 hover:cursor-pointer"/>
            <button className="bg-bg-light-secondary hover:bg-bg-light-secondary hover:shadow-lg px-2 py-1.5  rounded-lg w-20 text-accents-deep cursor-pointer dark:bg-transparent dark:hover:bg-accents-deep/50 dark:border-none dark:text-white" onClick={loginRouting}>Login</button>
            <button className="bg-accents-primary hover:bg-accents-deep hover:shadow-md px-2 py-1.5 rounded-lg w-20 cursor-pointer" onClick={signupRouting}>SignUp</button>
        </div>
    </header>
  )
}
