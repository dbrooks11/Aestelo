// Universal Header
import { type JSX} from "react";
import { ThemeButton } from "../../hooks/ThemeProvider";
import { Link, useNavigate, type NavigateFunction} from "react-router-dom";


const headerLinksStyle = "transition hover:scale-110 dark:hover:text-bg-light hover:text-black cursor-pointer"

export default function PublicHeader(): JSX.Element {
  const navigate: NavigateFunction = useNavigate()

  function loginRouting(): void{
      navigate('/login-email') 
  }

  function signupRouting(): void{
    navigate('/signup')
  }

  
  return (
    // todo: remove home links for production(home link will be logo)
    <header className='top-0 z-50 sticky flex items-center justify-between px-12 py-3 border-b-neutral-200 dark:border-b-black font-semibold dark:text-bg-light-secondary bg-bg-light-secondary/50 dark:bg-charcoal/65 backdrop-blur-lg' >
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

        {/* Regular Header for Public pages */}
        <div className="hidden md:flex gap-4 text-white justify-end min-w-1/3 xs:max-md:hidden">
            <ThemeButton className="flex justify-center items-center hover:bg-accents-primary/20 rounded-full w-10 h-10 text-black dark:text-white transition-colors duration-300 hover:cursor-pointer bg-transparent"/>
            <button className="bg-bg-light-secondary hover:bg-bg-light-secondary hover:shadow-lg px-2 py-1.5  rounded-lg w-20 text-accents-deep cursor-pointer dark:bg-transparent dark:hover:bg-accents-deep/50 dark:border-none dark:text-white" onClick={loginRouting}>Login</button>
            <button className="bg-accents-primary hover:bg-accents-deep hover:shadow-md px-2 py-1.5 rounded-lg w-20 cursor-pointer" onClick={signupRouting}>SignUp</button>
        </div>
    </header>
  )
}
