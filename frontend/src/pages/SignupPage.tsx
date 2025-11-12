import { useState, type JSX } from "react";
import { useFormStatus } from "react-dom";
import { useNavigate } from "react-router-dom";
import { appConfig } from "../config";

export default function SignupPage(): JSX.Element {

    const navigate = useNavigate()
    const [error, setError] = useState<string>("")
    

    async function signUp(formData: FormData): Promise<void>{
        const email: FormDataEntryValue | null = formData.get("email")
        const password: FormDataEntryValue | null  = formData.get("password")
        const confirm_password: FormDataEntryValue | null  = formData.get("confirm_password")

        if (!appConfig.API_URL) {
                throw new Error('Api misconifgured')
            }

        try{
            const response: Response = await fetch(`${appConfig.API_URL}/auth/signup`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                credentials: 'omit',
                body: JSON.stringify({
                    email,
                    password,
                    confirm_password
                })
            })

            const data = await response.json()

            if (response.ok){
                console.log(data.message)
                navigate('/login-email')
            }else{
                setError(data.error)
                throw new Error(error)
            }
        } catch (error){
            console.log(error)
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
                <input type="email" name="email" id="email" required></input>

                <label htmlFor="password">Password</label>
                <input type="text" name="password" id="password" required></input>

                <label htmlFor="confirm_password">Confirm Password</label>
                <input type="password" name="confirm_password" id="confirm_password" required></input>

                <SubmitButton/>
            </form>
        </section>
  )
}
