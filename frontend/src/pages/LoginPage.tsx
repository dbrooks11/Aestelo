import { useState, type JSX} from "react";
import { LoaderCircle, Eye, EyeClosed } from "lucide-react";
import { useFormStatus } from "react-dom";
import { Link, type NavigateFunction } from "react-router-dom";
import ToasterCustom from "../components/Toast";
import { publicInstance } from "../util/axiosHelpers";
import { useNavigate } from "react-router-dom";


export default function LoginPage({isEmail}:{isEmail: boolean}): JSX.Element {
    const navigate: NavigateFunction = useNavigate()
    const [showPassword, setShowPassword] = useState<boolean>(false)
    const[emailState, setEmailState] = useState<string | undefined>("")
    const [usernameState, setUsernameState] = useState<string | undefined>("")

    const loginMethod = isEmail ? "email" : "username"
    const alternateLoginMethod = isEmail ? "username" : "email"


    async function login(formData: FormData): Promise<void>{
        
        setEmailState(formData.get("email")?.toString())
        setUsernameState(formData.get("username")?.toString())
        try{ 
            const response = await publicInstance.post("/auth/login", formData)

            if(response.status === 200){
                navigate('/profile/me')
            }
        }catch(error){
            console.error("Login failed", error)
        }
    }

    //TODO: turn this into reusable component
    function SubmitButton(): JSX.Element{
        const {pending}:{pending:boolean} = useFormStatus()
        return(
            <button className="flex justify-center items-center gap-3 bg-accents-primary hover:bg-accents-deep hover:shadow-md mt-4 py-2 rounded-md font-semibold text-white text-xl transition hover:-translate-y-1 cursor-pointer" disabled = {pending}>{!pending ? null : <LoaderCircle className="animate-spin"/>} {!pending ? "Login" : "Logging in..."}</button>
        )

    }

    function showPasswords(){
        setShowPassword((show)=>{
            return !show
        })
    }

  return (
    <main className="flex flex-1 justify-center items-center py-2">
        <section className="flex flex-col justify-center items-center md:shadow-xl py-12 md:border md:border-bg-light-tertiary md:dark:border-slate md:rounded-lg w-full md:w-3/6 dark:text-neutral-300">
            
            {/* Header */}
            <h1 className="font-bold dark:text-bg-light text-2xl">Login</h1>
            
            {/* Login Form */}
            <form action={login} className="flex flex-col my-8 w-2/5" aria-label="Login Form">

                {/*  Honeypot Field (Hidden for Security)  */}
                <div className="-top-[9999px] -left-[9999px] absolute w-0 h-0" aria-hidden="true">
                    <label htmlFor="name" className="w-0 h-0"></label>
                    <input 
                        className="bg-transparent w-0 h-0 overflow-hidden cursor-none" 
                        type="text" 
                        id='name' 
                        name='name' 
                        autoComplete="off" 
                        tabIndex={-1} 
                    />
                </div>

                {/*  Email/Username Field  */}
                <div className="flex flex-col gap-2 mb-7">
                    <label htmlFor={loginMethod}>
                        {loginMethod.charAt(0).toUpperCase() + loginMethod.slice(1)}
                    </label>
                    <input 
                        className="border-neutral-500/30 focus:border-accents-primary border-b-2 focus:outline-none"
                        type={isEmail ? 'email' : 'text'}
                        name={loginMethod} 
                        id={loginMethod} 
                        autoComplete={loginMethod} 
                        defaultValue={isEmail ? emailState : usernameState}
                        placeholder={`Enter ${loginMethod}`}
                        required
                        aria-required="true"
                    />
                </div>

                {/* Password Field */}
                <div className="relative flex flex-col gap-2 mb-7">
                    <label htmlFor="password">Password</label>
                    <input 
                        className="pr-8 border-neutral-500/30 focus:border-accents-primary border-b-2 focus:outline-none"
                        type={showPassword ? "text" : "password"} 
                        name="password" 
                        id="password" 
                        autoComplete="current-password" 
                        placeholder="Enter password" 
                        required
                        aria-required="true"
                    />
                    <button 
                        type="button" 
                        tabIndex={-1} 
                        onClick={showPasswords} 
                        className="right-0 bottom-1 absolute flex justify-center items-center hover:bg-bg-light-tertiary hover:dark:bg-slate/60 dark:bg-charcoal hover:shadow-sm p-0.5 rounded-md w-6 text-black dark:text-stone-400 cursor-pointer" 
                        aria-label={showPassword ? "Show password" : "Hide password"}
                    >
                        {showPassword ? <Eye className="w-full h-full" aria-hidden="true"/> : <EyeClosed className="w-full h-full" aria-hidden="true"/>}
                    </button>
                </div>

                {/* Submit Action */}
                <SubmitButton/>
            </form>

            {/* Alternative Login Link */}
            <Link 
                className="flex w-fit text-sm" 
                to={`/login-${alternateLoginMethod}`}
                aria-label={`Switch to login with ${alternateLoginMethod}`}
            >
                Log in with {alternateLoginMethod}
            </Link>
        </section>
        <ToasterCustom toasterId='login'/>
    </main>
  )
}


