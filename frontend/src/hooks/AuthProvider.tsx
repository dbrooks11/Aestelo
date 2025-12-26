import { useEffect, useState, type ReactNode, type JSX } from "react";
import { protectedInstance } from "../util/axios_api_helpers";
import { AuthContext, type ProfileDataMinimal, type AuthContextType } from "../context/AuthContext";


export default function AuthProvider({ children }: {children: ReactNode}): JSX.Element {

    const [user, setUser] = useState<ProfileDataMinimal | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(true);
    

    //TODO: potential idea - use cookies with login value (true or false) to indicate if user is logged)
    const checkAuth = async () =>{
        try{
            const response = await protectedInstance.get('/auth/authenticate')

            if (response.status === 200){
                setUser(response.data)
            }

        }catch(error){
            console.log(error)
            setUser(null)
        }
        finally{
            setIsLoading(false)
        }
    }

    useEffect(() => {
        checkAuth()
    }, [])

    useEffect(() => {
        const authInterceptor = protectedInstance.interceptors.response.use(
            (response) => response,
            (error) => {
                
                if (error.response?.status === 401){
                    console.warn("Session expired or invalid. Loggin out...")
                    setUser(null)

                }
                return Promise.reject(error)
            }
        )
    
        return () => {
            protectedInstance.interceptors.response.eject(authInterceptor)
        }
    }, [setUser]);


    const value: AuthContextType = {
        user,
        isLoading,
        isAuthenticated: user ? true : false,
        checkAuth,
        setUser,
    }

    return (
        <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
    )
}
