import { use, createContext, type PropsWithChildren } from "react";
import { useStorageState } from "@/state/useStorageState";
import { protectedInstance } from "@/config/axios";
import { appConfig } from "@/config/api";
import { LoginFormData } from "@/app/login";

const AuthContext = createContext<{
    login: (value: LoginFormData) => void;
    signOut: () => void;
    session?: string | null;
    isLoading: boolean | null;
} | null>(null);


export function useSession() {
    const value = use(AuthContext);
    if (!value) {
        throw new Error('useSession must be wrapped in a <SessionProvider/>');
    }

    return value;
}

export function SessionProvider({ children }: PropsWithChildren) {
    const [[isLoading, session], setSession] = useStorageState('session');

    return (
        <AuthContext.Provider
            value={{
                login: async (value) => {
                    try {
                        const response = await protectedInstance.post(`${appConfig.API_URL}/auth/login`, value);
                        
                        setSession(response.data.session)
                    } catch (error) {
                        console.log("Api url", appConfig.API_URL)
                        console.error('Failed to Login')
                    }
                },
                signOut: async () => {
                    try {
                        await protectedInstance.post(`${appConfig.API_URL}/auth/logout`)
                        setSession(null)
                    } catch (error) {
                        console.error('Failed to Logout')
                    }    
                },
                session,
                isLoading
            }}>
                {children}
        </AuthContext.Provider>
    )
}