import { useState, type JSX } from "react";
import { LoaderCircle } from "lucide-react";
import { useFormStatus } from "react-dom";
import { useNavigate, type NavigateFunction, Link } from "react-router-dom";
import { AxisErrorHelper, loginInstance } from "../util/axios_api_helpers";


export default function LoginPage({isEmail}:{isEmail: boolean}): JSX.Element {
    const navigate: NavigateFunction = useNavigate()


    const[emailState, setEmailState] = useState<string | undefined>("")
    const [usernameState, setUsernameState] = useState<string | undefined>("")
    const [error, setError] = useState<string | null>("")


    async function login(formData: FormData): Promise<void>{
        const email: FormDataEntryValue | null = formData.get('email') ? formData.get('email') : null
        const username: FormDataEntryValue | null = formData.get('username') ? formData.get('username') : null
        const password: FormDataEntryValue | null = formData.get('password')

        if(email) setEmailState(email.toString())
        else setUsernameState(username?.toString())

        const body = {
            ...(email ? {email} : {username}),
            password
        }

        try{ 
            const response = await loginInstance.post(`/auth/login-${email ? 'email' : 'username'}`, body)

            const data = response.data

            if(response.status === 200){
                console.log(data.message)
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
            <button className="authenticated_forms_button" disabled = {pending}>{!pending ? null : <LoaderCircle className="animate-spin"/>} {!pending ? "Login" : "Logging in..."}</button>
        )

    }

  return (
    <main className="authenticated_forms_main_container">
        <section className="authenticated_forms_section_container">
            <h1 className="authenticated_forms_header">Login</h1>
            {error ? <span id='error' className="authenticated_forms_error">{error.split('.')[0]}</span>: null}
            <form action = {login} className="authenticated_forms_form">
                <div className="authenticated_forms_field_container">
                    <label htmlFor={isEmail ? "email" : "username"}>{isEmail ? "Email" : "Username"}</label>
                    <input type={isEmail ? "email" : "text"} name={isEmail ? "email" : "username"} id={isEmail ? "email" : "username"} autoComplete={isEmail ? "email" : "username"} defaultValue={isEmail ? emailState : usernameState} className="authenticated_forms_input_field" placeholder="Enter email" required></input>
                </div>
                <div className="authenticated_forms_field_container">
                    <label htmlFor="password">Password</label>
                    <input type="password" name="password" id="password" autoComplete="current-password" className="authenticated_forms_input_field" placeholder="Enter password" required></input>
                </div>
                <SubmitButton/>
            </form>
            <Link className="text-sm flex w-fit" to={`/login-${isEmail ? 'username': 'email'}`}>Log in with {isEmail ? 'username' : 'email'}</Link>
        </section>
    </main>
  )
}


