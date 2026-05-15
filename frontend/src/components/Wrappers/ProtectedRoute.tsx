import { Outlet } from "react-router-dom";
import { useState, type JSX,} from "react";
import MainFloatingNavBar from "../MainFloatingNavBar";
import CreateSpotForm from "../Forms/CreateSpotForm/CreateSpotForm";
import GlobalProgressTaskDrawer from "../GlobalTaskProgressDrawer";


export type CreateSpotFormModalOpenType = boolean
export type SpotAndVisitProgressType = Array<object>

export default function ProtectedRoute(): JSX.Element{
    const [isCreateSpotModalOpen, setIsCreateSpotModalOpen] = useState<CreateSpotFormModalOpenType>(false)

    return (
    <>
        <div className="flex-1 flex flex-col">
            <Outlet/>
        </div>
        <MainFloatingNavBar openModal={() => setIsCreateSpotModalOpen(true)}/>
        <CreateSpotForm isCreateSpotModalOpen={isCreateSpotModalOpen} setIsCreateSpotModalOpen={setIsCreateSpotModalOpen} 
        />
        <GlobalProgressTaskDrawer/>
    </>
    
)
}