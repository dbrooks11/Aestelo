import { Navigate, Outlet, useLocation } from "react-router-dom";
import { type JSX } from "react";
import { useAuth } from "../context/AuthContext";

export default function ProtectedRoute(): JSX.Element{
    const {isAuthenticated, isLoading} = useAuth()
    const location = useLocation()

    if (isLoading){
        return (
        <div>Loading....</div>
    )
    }

    if(!isAuthenticated){
        return <Navigate to="/login" state={{from: location}} replace/>
    }

    return <Outlet/>
}