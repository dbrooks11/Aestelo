import { useState, type JSX } from "react";
import { useFormStatus } from "react-dom";
import { useNavigate, type NavigateFunction } from "react-router-dom";
import { appConfig } from "../config";

export default function LoginPage({isEmail}:{isEmail: boolean}): JSX.Element {
    const navigate: NavigateFunction = useNavigate()

    const [emailOrUsername, setEmailOrUsername] = useState<string | undefined>("")
    const [error, setError] = useState<string>("")

    async function login(formData: FormData): Promise<void>{
        const email: FormDataEntryValue | null = formData.get('email') ? formData.get('email') : null
        const username: FormDataEntryValue | null = formData.get('username') ? formData.get('username') : null
        const password: FormDataEntryValue | null = formData.get('password')

        setEmailOrUsername(email ? email.toString() : username?.toString())

        const body = {
            ...(email ? {email} : {username}),
            password
        }

        try{ 
            const response: Response = await fetch(`${appConfig.API_URL}/auth/login-${email ? "email" : "username"}`, {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                credentials: "include",
                body: JSON.stringify(body)
            })

            const data = await response.json()

            if (response.ok){
                console.log(data.message)
                navigate('/') //todo: Set his to profile page (home page is only for testing)
            }
            else{
                setError(data.error)
                throw new Error(error)
            }
        }
        catch(error){
            console.error(error)
        }
    }

    function SubmitButton(): JSX.Element{
        const {pending}:{pending:boolean} = useFormStatus()
        return(
            <button disabled = {pending}>{!pending ? "Login" : "Logging in..."}</button>
        )

    }

  return (
    <section>
        <h1>Login</h1>
        {error ? error : null}
        <form action = {login}>
            <label htmlFor={isEmail ? "email" : "username"}>{isEmail ? "Email" : "Username"}</label>
            <input type={isEmail ? "email" : "text"} name={isEmail ? "email" : "username"} id={isEmail ? "email" : "username"} autoComplete={isEmail ? "email" : "username"} defaultValue={emailOrUsername ? emailOrUsername : undefined}required></input>

            <label htmlFor="password">Password</label>
            <input type="password" name="password" id="password" autoComplete="current-password" required></input>
            <SubmitButton/>
        </form>
    </section>
  )
}


