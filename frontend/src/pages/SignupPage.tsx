import { useState, type JSX } from "react";
import { LoaderCircle, Eye, EyeClosed } from "lucide-react";
import { AxiosErrorHelper, signupInstance } from "../util/axios_api_helpers";
import { useFormStatus } from "react-dom";
import { useNavigate, type NavigateFunction } from "react-router-dom";
import type { AxiosResponse} from "axios";
import ToasterCustom from "../components/Toast";
import toast from "react-hot-toast";


const inputFieldsStyle = "border-neutral-500/30 focus:border-accents-primary border-b-2 focus:outline-none"
const showPassStyle = "absolute right-0 bottom-1 w-6 p-0.5 rounded-md text-black hover:bg-bg-light-tertiary dark:bg-charcoal hover:dark:bg-slate/60 cursor-pointer dark:text-stone-400 flex items-center justify-center hover:shadow-sm"


export default function SignupPage(): JSX.Element {

    const navigate: NavigateFunction = useNavigate()
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
                navigate('/login-email')
                toast.success(data.message, {
                    toasterId: 'login'
                })
            }
        } catch (error: unknown){
            const newError = AxiosErrorHelper(error)
            toast.error(newError, {
                toasterId: 'signup'
            })

      }
    }

    function SubmitButton(): JSX.Element{
        const {pending} = useFormStatus()

        return(
            <button className="flex justify-center items-center gap-3 bg-accents-primary hover:bg-accents-deep hover:shadow-md mt-4 py-2 rounded-md font-semibold text-white text-xl transition hover:-translate-y-1 cursor-pointer" disabled = {pending}>{!pending ? null: <LoaderCircle className="animate-spin"/>} {!pending ? 'Sign Up' : 'Signing Up...'}</button>
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
    <main className="flex flex-1 justify-center items-center py-2">
        <section className="flex flex-col justify-center items-center md:shadow-xl py-12 md:border md:border-bg-light-tertiary md:dark:border-slate md:rounded-lg w-full md:w-3/6 dark:text-neutral-300">
        
            {/* Header */}
            <h1 className="font-bold dark:text-bg-light text-2xl">Sign Up</h1>

            {/* --- Signup Form --- */}
            <form action={signUp} className="flex flex-col my-8 w-2/5" aria-label="Sign Up Form">

                {/* --- Honeypot Field (Hidden for Security) --- */}
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

                {/* --- Email Field --- */}
                <div className="flex flex-col gap-2 mb-7">
                    <label htmlFor="email">Email</label>
                    <input 
                        className={inputFieldsStyle} 
                        type="email" 
                        name="email" 
                        id="email" 
                        autoComplete="email" 
                        defaultValue={email} 
                        placeholder="Enter email"
                        required
                        aria-required="true" 
                    />
                </div>

                {/* --- Password Field --- */}
                <div className="relative flex flex-col gap-2 mb-7">
                    <label htmlFor="password">Password</label>
                    <input 
                        className={inputFieldsStyle} 
                        type={showPasswordOne} 
                        name="password" 
                        id="password" 
                        placeholder="Enter password"
                        required
                        aria-required="true"
                    />
                    <button 
                        type="button" 
                        tabIndex={-1} 
                        onClick={showPasswordsOne} 
                        className={showPassStyle} 
                        aria-label={showPasswordOne === 'text' ? "Hide password" : "Show password"}
                    >
                        {showPasswordOne === 'text' ? <EyeClosed className="w-full h-full" aria-hidden="true"/> : <Eye className="w-full h-full" aria-hidden="true"/>}
                    </button>
                </div>

                {/* --- Confirm Password Field --- */}
                <div className="relative flex flex-col gap-2 mb-7">
                    <label htmlFor="confirm_password">Confirm Password</label>
                    <input 
                        className={inputFieldsStyle} 
                        type={showPasswordTwo} 
                        name="confirm_password" 
                        id="confirm_password" 
                        placeholder="Re-enter password" 
                        required
                        aria-required="true"
                    />
                    <button 
                        type="button" 
                        tabIndex={-1} 
                        onClick={showPasswordsTwo} 
                        className={showPassStyle} 
                        aria-label={showPasswordTwo === 'text' ? "Hide confirm password" : "Show confirm password"}
                    >
                        {showPasswordTwo === 'text' ? <EyeClosed className="w-full h-full" aria-hidden="true"/> : <Eye className="w-full h-full" aria-hidden="true"/>}
                    </button>
                </div>

                {/* --- Submit Action --- */}
                <SubmitButton/>
            </form>
        </section>
        <ToasterCustom toasterId='signup'/>
    </main>
  )
}
