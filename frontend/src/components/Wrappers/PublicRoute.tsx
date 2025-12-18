import { Outlet } from "react-router-dom";
import { type JSX, type Dispatch, type SetStateAction} from "react";
import PublicHeader from "../Header/Header";


type PublicRouteProps = {
    theme: 'light' | 'dark'
    setTheme: Dispatch<SetStateAction<'light' | 'dark'>>
}

export default function PublicRoute ({theme, setTheme}: PublicRouteProps): JSX.Element {
    return (
        <>
            <PublicHeader theme = {theme} setTheme={setTheme}/>
            <div className="flex-1 flex flex-col">
                <Outlet/>
            </div> 
        </>
        
    )
}