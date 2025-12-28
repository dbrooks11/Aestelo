import { createContext, useContext} from "react";
import { type ProfileDataType } from "../pages/ProfilePage";


export type ProfileDataMinimal = Pick<ProfileDataType, 'id' | 'username' | 'profile_photo_url'>

export type AuthContextType = {
    user: ProfileDataMinimal | null,
    checkAuth: () => Promise<void>,
    setUser: (user: ProfileDataMinimal | null) => void,
    isLoading: boolean,
    isAuthenticated: boolean,
    
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined)


export const useAuth = (): AuthContextType=> {
    const context: AuthContextType | undefined = useContext(AuthContext)
    if(!context){
        throw new Error("useAuth must be used within an AuthProvider")
    }
    return context
}