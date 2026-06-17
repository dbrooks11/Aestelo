import { use, createContext, type PropsWithChildren } from "react";
import { useStorageState } from "@/state/use-storage-state";
import { protectedInstance, publicInstance } from "@/config/axios";
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
                        const response = await publicInstance.post('/auth/login', value);
                        setSession(response.data.session)
                    } catch (error) {
                        console.error('Failed to Login', error)
                    }
                },
                signOut: async () => {
                    try {
                        await protectedInstance.post('/auth/sign-out')
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