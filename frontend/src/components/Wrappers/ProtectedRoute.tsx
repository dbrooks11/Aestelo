import { Navigate, Outlet, useLocation } from "react-router-dom";
import { type JSX,} from "react";
import { useAuth } from "../../context/AuthContext";
import MainFloatingNavBar from "../MainFloatingNavBar";


export default function ProtectedRoute(): JSX.Element{
    const {isAuthenticated, isLoading} = useAuth()
    const location = useLocation()

    if (isLoading){
        return (
        <></>
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
        <MainFloatingNavBar/>
    </>
    
)
}