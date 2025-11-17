import { useState, type JSX } from "react";
import { LoaderCircle } from "lucide-react";
import { AxisErrorHelper, signupInstance } from "../util/axios_api_helpers";
import { useFormStatus } from "react-dom";
import { useNavigate, type NavigateFunction } from "react-router-dom";
import type { AxiosResponse} from "axios";

export default function SignupPage(): JSX.Element {

    const navigate: NavigateFunction = useNavigate()
    const [error, setError] = useState<string | null>("")
    const [email, setEmail] = useState<string | undefined>("")
    

    async function signUp(formData: FormData): Promise<void>{
        const email: FormDataEntryValue | null = formData.get("email")
        const password: FormDataEntryValue | null  = formData.get("password")
        const confirm_password: FormDataEntryValue | null  = formData.get("confirm_password")

        const stringEmail: string | undefined = email?.toString()
        setEmail(stringEmail)

        try{
            const response: AxiosResponse = await signupInstance.post('/auth/signup', {
                email,
                password,
                confirm_password
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

    
  return (
    <main className="authenticated_forms_main_container">
        <section className="authenticated_forms_section_container">
            <h1 className="authenticated_forms_header">Sign Up</h1>
            {error ? <span id='error' className="authenticated_forms_error">{error.split('.')[0]}</span>: null}
            <form action={signUp} className="authenticated_forms_form">
                <div className="authenticated_forms_field_container">
                    <label htmlFor="email">Email</label>
                    <input className="authenticated_forms_input_field" type="email" name="email" id="email" autoComplete="email" defaultValue={email} placeholder="Enter email"required></input>
                </div>
                <div className="authenticated_forms_field_container">
                    <label htmlFor="password">Password</label>
                    <input className="authenticated_forms_input_field" type="password" name="password" id="password" placeholder="Enter password"required></input>
                </div>
                <div className="authenticated_forms_field_container">
                    <label htmlFor="confirm_password">Confirm Password</label>
                    <input className="authenticated_forms_input_field" type="password" name="confirm_password" id="confirm_password" placeholder="Re-enter password" required></input>
                </div>
                <SubmitButton/>
            </form>
        </section>
    </main>
  )
}
