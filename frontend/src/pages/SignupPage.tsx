import { useState, type JSX } from "react";
import { LoaderCircle, Eye, EyeClosed } from "lucide-react";
import { AxisErrorHelper, signupInstance } from "../util/axios_api_helpers";
import { useFormStatus } from "react-dom";
import { useNavigate, type NavigateFunction } from "react-router-dom";
import type { AxiosResponse} from "axios";

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
            console.log("form rejected. bot detected")
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
            <button className="authenticated_forms_button" disabled = {pending}>{!pending ? null: <LoaderCircle className="animate-spin"/>} {!pending ? 'Sign Up' : 'Signing Up...'}</button>
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
    <main className="authenticated_forms_main_container">
        <section className="authenticated_forms_section_container">
            {/* Signup Header */}
            <h1 className="authenticated_forms_header">Sign Up</h1>

            {/* Error show */}
            {error ? <span id='error' className="authenticated_forms_error">{error.split('.')[0]}</span>: null}

            {/* Signup Form */}
            <form action={signUp} className="authenticated_forms_form">

                {/* Honeypot field */}
                <div className="w-0 h-0 absolute -left-[9999px] -top-[9999px]" aria-hidden aria-label="ignore this">
                  <label htmlFor="name" className="w-0 h-0"></label>
                  <input className="overflow-hidden bg-transparent w-0 h-0 cursor-none" type="text" id='name' name='name' autoComplete="off" aria-label="skip this input. it is for non-real users" tabIndex={-1}></input>
                </div>

                {/* Email field */}
                <div className="authenticated_forms_field_container">
                    <label htmlFor="email">Email</label>
                    <input className="authenticated_forms_input_field" type="email" name="email" id="email" autoComplete="email" defaultValue={email} placeholder="Enter email"required></input>
                </div>

                {/* Password field */}
                <div className="authenticated_forms_field_container relative">
                    <label htmlFor="password">Password</label>
                    <input className="authenticated_forms_input_field" type={showPasswordOne} name="password" id="password" placeholder="Enter password"required></input>
                    <button type="button" tabIndex={-1} onClick={showPasswordsOne} className="authenticated_forms_showpass" aria-label="show or hide password button">{showPasswordOne === 'text' ? <EyeClosed className="w-full h-full"/> : <Eye className="w-full h-full"/>}</button>
                </div>

                {/* Re-confirm password field */}
                <div className="authenticated_forms_field_container relative">
                    <label htmlFor="confirm_password">Confirm Password</label>
                    <input className="authenticated_forms_input_field" type={showPasswordTwo} name="confirm_password" id="confirm_password" placeholder="Re-enter password" required></input>
                    <button type="button" tabIndex={-1} onClick={showPasswordsTwo} className="authenticated_forms_showpass" aria-label="show or hide password button">{showPasswordTwo === 'text' ? <EyeClosed className="w-full h-full"/> : <Eye className="w-full h-full"/>}</button>
                </div>

                {/* Submit button component */}
                <SubmitButton/>
            </form>
        </section>
    </main>
  )
}
