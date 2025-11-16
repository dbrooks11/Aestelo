// Universal Header
import { type JSX, type Dispatch, type SetStateAction} from "react";
import {motion, AnimatePresence} from 'framer-motion'
import { Moon, Sun } from "lucide-react";
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

  

  return (
    // todo: remove home links for production(home link will be logo)
    <header className="top-0 z-50 sticky flex justify-between items-center bg-bg-light/50 dark:bg-charcoal/65 backdrop-blur-lg px-8 py-3  border-b-neutral-200 dark:border-b-black font-semibold dark:text-bg-light-secondary">
        <span className="text-3xl text-black dark:text-white">Aeste<span className="text-accents-primary">lo</span></span>
        <nav className="flex gap-8 dark:text-mid-gray text-black/75 text-sm mx-5">
          <Link className="dark:hover:text-bg-light hover:text-black hover:underline hover:underline-offset-4 cursor-pointer" to="/">Home</Link>
          <Link className="dark:hover:text-bg-light hover:text-black hover:underline hover:underline-offset-4 cursor-pointer" to="/about">About</Link>
          <Link className="dark:hover:text-bg-light hover:text-black hover:underline hover:underline-offset-4 cursor-pointer" to="/expore">Explore</Link>
        </nav>
        {!isAuthenticated ? <div className="flex gap-4 text-white">
            <button className="flex justify-center items-center hover:bg-accents-primary/20 rounded-full w-10 h-10 text-black dark:text-white transition-colors duration-300 hover:cursor-pointer" onClick={setThemeHeader}>
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
            <button className="bg-bg-light-secondary hover:bg-accents-deep hover:shadow-md px-2 py-1.5 border border-accents-deep rounded-lg w-20 text-accents-deep hover:text-white cursor-pointer dark:bg-transparent dark:hover:bg-accents-deep/50 dark:border-none dark:text-white" onClick={loginRouting}>Login</button>
            <button className="bg-accents-primary hover:bg-accents-deep hover:shadow-md px-2 py-1.5 border border-accents-deep rounded-lg w-20 cursor-pointer" onClick={signupRouting}>SignUp</button>
        </div>: null}
        {isAuthenticated ? <nav className="flex justify-between">
            <Link to="/profile/me">Profile</Link>
            <Link to="/post/feed">Feed</Link>
            <button onClick={logout}>Logout</button>
        </nav>: null}
    </header>
  )
}
