import { useState, type JSX } from "react";
import { AxisErrorHelper, signupInstance } from "../util/axios_api_helpers";
import { useFormStatus } from "react-dom";
import { useNavigate, type NavigateFunction } from "react-router-dom";
import type { AxiosResponse} from "axios";

export default function SignupPage(): JSX.Element {

    const navigate: NavigateFunction = useNavigate()
    const [error, setError] = useState<string | null>("")
    

    async function signUp(formData: FormData): Promise<void>{
        const email: FormDataEntryValue | null = formData.get("email")
        const password: FormDataEntryValue | null  = formData.get("password")
        const confirm_password: FormDataEntryValue | null  = formData.get("confirm_password")

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
            AxisErrorHelper(error, setError, "Sign Up")
      }
    }

    function SubmitButton(): JSX.Element{
        const {pending} = useFormStatus()

        return(
            <button disabled = {pending}>{!pending ? 'Sign Up' : 'Signing Up...'}</button>
        )
    }


  return (
        <section>
            <h1>Sign Up</h1>
            {error ? <span>{error}</span>: null}
            <form action={signUp} className="signup-form">
                <label htmlFor="email">Email</label>
                <input type="email" name="email" id="email" autoComplete="email" required></input>

                <label htmlFor="password">Password</label>
                <input type="password" name="password" id="password" required></input>

                <label htmlFor="confirm_password">Confirm Password</label>
                <input type="password" name="confirm_password" id="confirm_password" required></input>

                <SubmitButton/>
            </form>
        </section>
  )
}
