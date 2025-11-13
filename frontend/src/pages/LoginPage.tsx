import { useState, type JSX } from "react";
import { useFormStatus } from "react-dom";
import { useNavigate, type NavigateFunction } from "react-router-dom";
import { AxisErrorHelper, loginInstance } from "../util/axios_api_helpers";


export default function LoginPage({isEmail}:{isEmail: boolean}): JSX.Element {
    const navigate: NavigateFunction = useNavigate()

    const [emailOrUsername, setEmailOrUsername] = useState<string | undefined>("")
    const [error, setError] = useState<string | null>("")

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
            const response = await loginInstance.post(`/auth/login-${email ? 'email' : 'username'}`, body)

            const data = response.data

            if(response.status === 200){
                console.log(data.message)
                navigate('/') //todo: change to profile page
            }
        }
        catch(error: unknown){
            AxisErrorHelper(error, setError, "Log in")
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


