import { useEffect, useState, type ReactNode, type JSX } from "react";
import { AuthContext, type AuthContextType } from "../context/AuthContext";
import { csrfRefreshToken } from "../util/cookieHandlers";
import { protectedInstance } from "../util/axiosHelpers";
import axios from "axios";


export default function AuthProvider({ children }: {children: ReactNode}): JSX.Element {

    const [user, setUser] = useState<boolean | null>(false);
    const [isLoading, setIsLoading] = useState<boolean>(true);
    


    useEffect(() => {
        const authInterceptor = protectedInstance.interceptors.response.use(
            (response) => response,
            async (error) => {
                const originalRequest = error.config;
                
                if ([401].includes(error.response?.status) && !originalRequest._retry){
                    originalRequest._retry = true;
                    try{
                        const refreshResponse = await protectedInstance.post('/auth/refresh', {}, {
                            withCredentials: true,
                            headers: {
                                "X-CSRF-TOKEN": csrfRefreshToken()
                            }
                        })

                        if (refreshResponse.status === 200){
                            console.log("Refreshing session...")
                            originalRequest.headers["X-CSRF-TOKEN"] = csrfRefreshToken()
                            return axios(originalRequest)
                        }
                    }catch(error){
                        console.warn("Session expired. Logging out...")
                        setUser(false)
                        window.location.href = '/login-email'
                    }
                }
                return Promise.reject(error)
            }
        )
    
        return () => {
            axios.interceptors.response.eject(authInterceptor)
        }
    }, [setUser]);


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
