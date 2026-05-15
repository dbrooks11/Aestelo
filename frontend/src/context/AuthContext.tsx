import { createContext} from "react";

export type AuthContextType = {
    user: boolean | null,
    setUser: (user: boolean | null) => void,
    isLoading: boolean,
    isAuthenticated: boolean,
    
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined)