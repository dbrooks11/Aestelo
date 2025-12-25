import { useState, type JSX } from "react";
import { LoaderCircle, Eye, EyeClosed } from "lucide-react";
import { AxisErrorHelper, signupInstance } from "../util/axios_api_helpers";
import { useFormStatus } from "react-dom";
import { useNavigate, type NavigateFunction } from "react-router-dom";
import type { AxiosResponse} from "axios";


const inputFieldsStyle = "border-neutral-500/30 focus:border-accents-primary border-b-2 focus:outline-none"
const showPassStyle = "absolute right-0 bottom-1 w-6 p-0.5 rounded-md text-black hover:bg-bg-light-tertiary dark:bg-charcoal hover:dark:bg-slate/60 cursor-pointer dark:text-stone-400 flex items-center justify-center hover:shadow-sm"


export default function SignupPage(): JSX.Element {

    const navigate: NavigateFunction = useNavigate()
    const [error, setError] = useState<string | null>("")
    const [email, setEmail] = useState<string | undefined>("")
    const [showPasswordOne, setShowPasswordOne] = useState("password")
    const [showPasswordTwo, setShowPasswordTwo] = useState("password")
    

    async function signUp(formData: FormData): Promise<void>{
        const name: FormDataEntryValue | null = formData.get("name")
        const email: FormDataEntryValue | null = formData.get("email")
        const password: FormDataEntryValue | null  = formData.get("password")
        const confirm_password: FormDataEntryValue | null  = formData.get("confirm_password")

        if(name?.toString().trim()) {
            return
        }
            

        const stringEmail: string | undefined = email?.toString()
        setEmail(stringEmail)

        try{
            const response: AxiosResponse = await signupInstance.post('/auth/signup', {
                email,
                password,
                confirm_password,
                ...(name ? {name} : {undefined}),
            })

            const data = response.data

            if (response.status === 201){
                console.log(data.message)
                navigate('/login-email')
            }
        } catch (error: unknown){
            (AxisErrorHelper(error, setError, "Sign Up"))
      }
    }

    function SubmitButton(): JSX.Element{
        const {pending} = useFormStatus()

        return(
            <button className="flex items-center justify-center gap-3 bg-accents-primary hover:bg-accents-deep hover:shadow-md py-2 mt-4 rounded-md font-semibold text-white text-xl transition hover:-translate-y-1 cursor-pointer" disabled = {pending}>{!pending ? null: <LoaderCircle className="animate-spin"/>} {!pending ? 'Sign Up' : 'Signing Up...'}</button>
        )
    }

    function showPasswordsOne(){
        setShowPasswordOne((type)=>{
            return type === 'text' ? 'password' : 'text'
        })
    }

    function showPasswordsTwo(){
        setShowPasswordTwo((type)=>{
            return type === 'text' ? 'password' : 'text'
        })
    }

    
  return (
    <main className="flex items-center justify-center flex-1 py-2">
        <section className="flex flex-col items-center justify-center w-full md:shadow-xl py-12 md:border md:dark:border-slate md:rounded-lg md:w-3/6 dark:text-neutral-300 md:border-bg-light-tertiary">
            {/* Signup Header */}
            <h1 className="font-bold dark:text-bg-light text-2xl">Sign Up</h1>

            {/* Error show */}
            {error ? <span id='error' className="bg-bg-light-tertiary mt-8 px-2 py-1 border border-neutral-200 rounded-xl font-medium text-sm dark:bg-mid-gray/10 dark:text-white/85">{error.split('.')[0]}</span>: null}

            {/* Signup Form */}
            <form action={signUp} className="flex flex-col my-8 w-2/5">

                {/* Honeypot field */}
                <div className="w-0 h-0 absolute -left-[9999px] -top-[9999px]" aria-hidden aria-label="ignore this">
                  <label htmlFor="name" className="w-0 h-0"></label>
                  <input className="overflow-hidden bg-transparent w-0 h-0 cursor-none" type="text" id='name' name='name' autoComplete="off" aria-label="skip this input. it is for non-real users" tabIndex={-1}></input>
                </div>

                {/* Email field */}
                <div className="flex flex-col gap-2 mb-7">
                    <label htmlFor="email">Email</label>
                    <input className={inputFieldsStyle} type="email" name="email" id="email" autoComplete="email" defaultValue={email} placeholder="Enter email"required></input>
                </div>

                {/* Password field */}
                <div className="flex flex-col gap-2 mb-7 relative">
                    <label htmlFor="password">Password</label>
                    <input className={inputFieldsStyle}  type={showPasswordOne} name="password" id="password" placeholder="Enter password"required></input>
                    <button type="button" tabIndex={-1} onClick={showPasswordsOne} className={showPassStyle} aria-label="show or hide password button">{showPasswordOne === 'text' ? <EyeClosed className="w-full h-full"/> : <Eye className="w-full h-full"/>}</button>
                </div>

                {/* Re-confirm password field */}
                <div className="flex flex-col gap-2 mb-7 relative">
                    <label htmlFor="confirm_password">Confirm Password</label>
                    <input className={inputFieldsStyle}  type={showPasswordTwo} name="confirm_password" id="confirm_password" placeholder="Re-enter password" required></input>
                    <button type="button" tabIndex={-1} onClick={showPasswordsTwo} className={showPassStyle} aria-label="show or hide password button">{showPasswordTwo === 'text' ? <EyeClosed className="w-full h-full"/> : <Eye className="w-full h-full"/>}</button>
                </div>

                {/* Submit button component */}
                <SubmitButton/>
            </form>
        </section>
    </main>
  )
}
