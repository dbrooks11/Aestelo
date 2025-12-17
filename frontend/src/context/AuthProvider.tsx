import { useEffect, useState, type ReactNode, type JSX } from "react";
import { protectedInstance } from "../util/axios_api_helpers";
import { type ProfileDataMinimal, type AuthContextType ,AuthContext } from "./AuthContext";


export default function AuthProvider({ children }: {children: ReactNode}): JSX.Element {

    const [user, setUser] = useState<ProfileDataMinimal | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(true);

    const checkAuth = async () =>{
        try{
            const response = await protectedInstance.get('/auth/authenticate')

            if (response.status === 200){
                setUser(response.data)
                
            }

        }catch(error){
            console.error(error)
        }
        finally{
            setIsLoading(false)
        }
    }

    useEffect(() => {
        checkAuth()
    }, [])



    const value: AuthContextType = {
        user,
        isLoading,
        isAuthenticated: user ? true : false,
        checkAuth,
        setUser
    }

    return (
        <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
    )
}
