import { useState, type JSX} from "react";
import { LoaderCircle, Eye, EyeClosed } from "lucide-react";
import { useFormStatus } from "react-dom";
import { useAuth } from "../context/AuthContext";
import { useNavigate, type NavigateFunction, Link } from "react-router-dom";
import { AxisErrorHelper, loginInstance } from "../util/axios_api_helpers";


export default function LoginPage({isEmail}:{isEmail: boolean}): JSX.Element {
    const navigate: NavigateFunction = useNavigate()

    const {checkAuth} = useAuth()
    
    const [showPassword, setShowPassword] = useState("password")
    const[emailState, setEmailState] = useState<string | undefined>("")
    const [usernameState, setUsernameState] = useState<string | undefined>("")
    const [error, setError] = useState<string | null>("")


    async function login(formData: FormData): Promise<void>{
        const name: FormDataEntryValue | null = formData.get("name") //for honey pot check
        const email: FormDataEntryValue | null = formData.get('email') ? formData.get('email') : null
        const username: FormDataEntryValue | null = formData.get('username') ? formData.get('username') : null
        const password: FormDataEntryValue | null = formData.get('password')

        if(name?.toString().trim()) return
        if(email) setEmailState(email.toString())
        else setUsernameState(username?.toString())

        const body = {
            ...(email ? {email} : {username}),
            password,
            ...(name ? {name} : {undefined}),
        }

        try{ 
            const response = await loginInstance.post(`/auth/login-${email ? 'email' : 'username'}`, body)

            const data = response.data

            if(response.status === 200){
                console.log(data.message)
                await checkAuth()
                navigate('/profile/me') 
            }
        }
        catch(error: unknown){
            AxisErrorHelper(error, setError, "Log in")
        }
    }

    function SubmitButton(): JSX.Element{
        const {pending}:{pending:boolean} = useFormStatus()
        return(
            <button className="flex items-center justify-center gap-3 bg-accents-primary hover:bg-accents-deep hover:shadow-md py-2 mt-4 rounded-md font-semibold text-white text-xl transition hover:-translate-y-1 cursor-pointer" disabled = {pending}>{!pending ? null : <LoaderCircle className="animate-spin"/>} {!pending ? "Login" : "Logging in..."}</button>
        )

    }

    function showPasswords(){
        setShowPassword((type)=>{
            return type === 'text' ? 'password' : 'text'
        })
    }

  return (
    <main className="flex items-center justify-center flex-1 py-2">
        <section className="flex flex-col items-center justify-center w-full md:shadow-xl py-12 md:border md:dark:border-slate md:rounded-lg md:w-3/6 dark:text-neutral-300 md:border-bg-light-tertiary">
            {/* Login Header */}
            <h1 className="font-bold dark:text-bg-light text-2xl">Login</h1>

            {/* Error Show */}
            {error ? <span id='error' className="bg-bg-light-tertiary mt-8 px-2 py-1 border border-neutral-200 rounded-xl font-medium text-sm dark:bg-mid-gray/10 dark:text-white/85">{error.split('.')[0]}</span>: null}

            {/* Login Form */}
            <form action = {login} className="flex flex-col my-8 w-2/5">

                {/* HoneyPot Field*/}
                <div className="w-0 h-0 absolute -left-[9999px] -top-[9999px]" aria-hidden aria-label="ignore this">
                  <label htmlFor="name" className="w-0 h-0"></label>
                  <input className="overflow-hidden bg-transparent w-0 h-0 cursor-none" type="text" id='name' name='name' autoComplete="off" aria-label="skip this input. it is for non-real users" tabIndex={-1}></input>
                </div>

                {/* Email field & Username field*/}
                <div className="flex flex-col gap-2 mb-7">
                    <label htmlFor={isEmail ? "email" : "username"}>{isEmail ? "Email" : "Username"}</label>
                    <input 
                    type={isEmail ? "text" : "text"}
                    name={isEmail ? "email" : "username"} 
                    id={isEmail ? "email" : "username"} 
                    autoComplete={isEmail ? "email" : "username"} 
                    defaultValue={isEmail ? emailState : usernameState} className="border-neutral-500/30 focus:border-accents-primary border-b-2 focus:outline-none" 
                    placeholder={isEmail ? "Enter email" : "Enter username"}
                    required>
                    </input>
                    
                </div>

                {/* Password field */}
                <div className="flex flex-col gap-2 mb-7 relative">
                    <label htmlFor="password">Password</label>
                    <input type={showPassword} name="password" id="password" autoComplete="current-password" className="border-neutral-500/30 focus:border-accents-primary border-b-2 focus:outline-none pr-8" placeholder="Enter password" required></input>
                    <button type="button" tabIndex={-1} onClick={showPasswords} className="absolute right-0 bottom-1 w-6 p-0.5 rounded-md text-black hover:bg-bg-light-tertiary dark:bg-charcoal hover:dark:bg-slate/60 cursor-pointer dark:text-stone-400 flex items-center justify-center hover:shadow-sm" aria-label="show or hide password button">{showPassword === 'text' ? <EyeClosed className="w-full h-full"/> : <Eye className="w-full h-full"/>}</button>
                </div>

                {/* Submit button component */}
                <SubmitButton/>
            </form>

            {/* Alternative login link */}
            <Link className="text-sm flex w-fit" to={`/login-${isEmail ? 'username': 'email'}`}>Log in with {isEmail ? 'username' : 'email'}</Link>
        </section>
    </main>
  )
}


