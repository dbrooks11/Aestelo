import { useState, type JSX} from "react";
import { LoaderCircle, Eye, EyeClosed } from "lucide-react";
import { useFormStatus } from "react-dom";
import { useNavigate, type NavigateFunction, Link } from "react-router-dom";
import { AxisErrorHelper, loginInstance } from "../util/axios_api_helpers";


export default function LoginPage({isEmail}:{isEmail: boolean}): JSX.Element {
    const navigate: NavigateFunction = useNavigate()


    const [showPassword, setShowPassword] = useState("password")
    const[emailState, setEmailState] = useState<string | undefined>("")
    const [usernameState, setUsernameState] = useState<string | undefined>("")
    const [error, setError] = useState<string | null>("")


    async function login(formData: FormData): Promise<void>{
        const name: FormDataEntryValue | null = formData.get("name")
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

    function showPasswords(){
        setShowPassword((type)=>{
            return type === 'text' ? 'password' : 'text'
        })
    }

  return (
    <main className="authenticated_forms_main_container">
        <section className="authenticated_forms_section_container">
            {/* Login Header */}
            <h1 className="authenticated_forms_header">Login</h1>

            {/* Error Show */}
            {error ? <span id='error' className="authenticated_forms_error">{error.split('.')[0]}</span>: null}

            {/* Login Form */}
            <form action = {login} className="authenticated_forms_form">

                {/* HoneyPot Field*/}
                <div className="w-0 h-0 absolute -left-[9999px] -top-[9999px]" aria-hidden aria-label="ignore this">
                  <label htmlFor="name" className="w-0 h-0"></label>
                  <input className="overflow-hidden bg-transparent w-0 h-0 cursor-none" type="text" id='name' name='name' autoComplete="off" aria-label="skip this input. it is for non-real users" tabIndex={-1}></input>
                </div>

                {/* Email field & Username field*/}
                <div className="authenticated_forms_field_container">
                    <label htmlFor={isEmail ? "email" : "username"}>{isEmail ? "Email" : "Username"}</label>
                    <input 
                    type={isEmail ? "text" : "text"}
                    name={isEmail ? "email" : "username"} 
                    id={isEmail ? "email" : "username"} 
                    autoComplete={isEmail ? "email" : "username"} 
                    defaultValue={isEmail ? emailState : usernameState} className="authenticated_forms_input_field" 
                    placeholder={isEmail ? "Enter email" : "Enter username"}
                    required>
                    </input>
                    
                </div>

                {/* Password field */}
                <div className="authenticated_forms_field_container relative">
                    <label htmlFor="password">Password</label>
                    <input type={showPassword} name="password" id="password" autoComplete="current-password" className="authenticated_forms_input_pass" placeholder="Enter password" required></input>
                    <button type="button" tabIndex={-1} onClick={showPasswords} className="authenticated_forms_showpass" aria-label="show or hide password button">{showPassword === 'text' ? <EyeClosed className="w-full h-full"/> : <Eye className="w-full h-full"/>}</button>
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


