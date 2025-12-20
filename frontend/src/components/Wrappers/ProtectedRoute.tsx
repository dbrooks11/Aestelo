import { Navigate, Outlet, useLocation } from "react-router-dom";
import { type JSX, type Dispatch, type SetStateAction} from "react";
import { useAuth } from "../../context/AuthContext";
import ProtectedHeader from "../Headers/HeaderAuth";

type ProtectedRouteProps = {
    theme: 'light' | 'dark'
    setTheme: Dispatch<SetStateAction<"light" | "dark">>
}


export default function ProtectedRoute({theme, setTheme}: ProtectedRouteProps): JSX.Element{
    const {isAuthenticated, isLoading} = useAuth()
    const location = useLocation()

    if (isLoading){
        return (
        <div>Loading....</div>
    )
    }

    if(!isAuthenticated){
        return <Navigate to="/login-email" state={{from: location}} replace/>
    }

    return (
    <>
        <div className="flex-1 flex flex-col">
            <Outlet/>
        </div>
    </>
    
)
}