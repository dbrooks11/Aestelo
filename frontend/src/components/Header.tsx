// Universal Header
import type { JSX } from "react";
import { Link, useNavigate, type NavigateFunction } from "react-router-dom";
import {AxisErrorHelperConsoleOnly, protectedInstance } from "../util/axios_api_helpers";


export default function Header(): JSX.Element {

  const navigate: NavigateFunction = useNavigate()

  async function logout(): Promise<void>{
  
    try{
      const response = await protectedInstance.post('auth/logout')

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
