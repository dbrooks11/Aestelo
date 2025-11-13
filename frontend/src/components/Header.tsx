// Universal Header
import type { JSX } from "react";
import { Link, useNavigate, type NavigateFunction } from "react-router-dom";
import { appConfig } from "../config";
import { csrfAccessToken } from "../util/cookie_helper";


export default function Header(): JSX.Element {

  const navigate: NavigateFunction = useNavigate()

  async function logout(): Promise<void>{
    const csrfToken: string | undefined = csrfAccessToken()

    const headers: HeadersInit = {
      ...(csrfToken && {'X-CSRF-TOKEN': csrfToken})
    }
    try{
      const response: Response = await fetch(`${appConfig.API_URL}/auth/logout`,{
        method: "POST",
        headers: headers,
        credentials: "include"
      })

      const data = await response.json()

      if(response.ok){
        console.log(data.message)
        navigate('/login-email')

      }else{
        throw new Error(data.error)
      }

    }catch(error){
      console.error(error)
    }

  }

  function loginRouting(): void{
    navigate('/login-email')
  }

  return (
    <header>
        <nav>
            <Link to="/">Home</Link>
            <Link to="/signup">SignUp</Link>
            <button onClick={loginRouting}>Login</button>
            <button onClick={logout}>Logout</button>
        </nav>
    </header>
  )
}
