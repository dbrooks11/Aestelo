import { Outlet } from "react-router-dom";
import { type JSX} from "react";
import PublicHeader from "../Headers/HeaderPublic";


export default function PublicRoute (): JSX.Element {
    return (
        <>
            <PublicHeader/>
            <div className="flex-1 flex flex-col">
                <Outlet/>
            </div> 
        </>
        
    )
}