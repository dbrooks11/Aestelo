// Universal Header
import type { JSX } from "react";
import { Link, useNavigate, type NavigateFunction } from "react-router-dom";
import {AxisErrorHelperConsoleOnly, protectedInstance } from "../util/axios_api_helpers";
import type { AxiosResponse } from "axios";


export default function Header({isAuthenticated}: {isAuthenticated: boolean}): JSX.Element {

  const navigate: NavigateFunction = useNavigate()

  async function logout(): Promise<void>{
  
    try{
      const response: AxiosResponse = await protectedInstance.post('auth/logout')

      const data = response.data

      if(response.status === 200){
        console.log(data.message)
        navigate('/login-email')
      }

    }catch(error: unknown){
      AxisErrorHelperConsoleOnly(error, "Log Out")
    }

  }

  function loginRouting(): void{
    navigate('/login-email')
  }

  function signupRouting(): void{
    navigate('/signup')
  }

  return (
    <header>
        {!isAuthenticated ? <nav>
            <Link to="/">Home</Link>
            <button onClick={signupRouting}>SignUp</button>
            <button onClick={loginRouting}>Login</button>
        </nav>: null}
        {isAuthenticated ? <nav>
            <Link to="/">Home</Link>
            <Link to="/profile/me">Profile</Link>
            <Link to="/post/feed">Feed</Link>
            <button onClick={logout}>Logout</button>
        </nav>: null}
    </header>
  )
}
