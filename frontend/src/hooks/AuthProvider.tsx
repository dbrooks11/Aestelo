import { useState, type ReactNode, type JSX } from "react";
import { AuthContext, type AuthContextType } from "../context/AuthContext";



export default function AuthProvider({ children }: {children: ReactNode}): JSX.Element {

    const [user, setUser] = useState<boolean | null>(false);
    const [isLoading, setIsLoading] = useState<boolean>(true);
    
    const value: AuthContextType = {
        user,
        isLoading,
        isAuthenticated: user ? true : false,
        setUser,
    }

    return (
        <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
    )
}
