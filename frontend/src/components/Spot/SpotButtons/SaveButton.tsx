import { useCallback, type Dispatch, type JSX, type SetStateAction } from "react";
import { Bookmark} from "lucide-react";
import SpotButtonBase from "./SpotButtonBase";
import { useSpotMutation } from "../../../hooks/SpotHooks/useSpotMutation";
import { AxiosErrorHelper, protectedInstance } from "../../../util/axios_api_helpers";

type SaveButton =  {
    setIsSavedState: Dispatch<SetStateAction<boolean>>
    isSavedState: boolean
    spotId: number
    saveCountState: number
    setSaveCountState: Dispatch<SetStateAction<number>>
    collections: Array<{is_default: boolean, id: number}>
}

export default function SaveButton(props: SaveButton): JSX.Element{

    const {updateSpotInCache} = useSpotMutation()

    const color = "#60a5fa"
    const fillColor = "#60a5fa"
    
    const onSaveClick = useCallback(async(collectionId: number | undefined) => {
        
        if(props.collections.length === 0) return

        const defaultCollection = props.collections.find((item) => item.is_default === true)
        const prevSaved = props.isSavedState

        console.log(collectionId)
        console.log(defaultCollection)

        if(collectionId === undefined && defaultCollection.id === undefined) return

        try{
            const response = await protectedInstance.post(`/collection/${collectionId ? collectionId : defaultCollection && defaultCollection.id}`, {
                spot_id: props.spotId
            })

            if(response.status === 200 || response.status === 201){
                const data = response.data
                const isSaved = data.saved
                const newSpotSaveCount = data.spot_save_count
                props.setIsSavedState(isSaved)
                props.setSaveCountState(newSpotSaveCount)
                updateSpotInCache(props.spotId, {
                    save_count: newSpotSaveCount,
                    is_saved: isSaved
                })
                console.log(data.message)
            }
        }catch(error){
            const newError = AxiosErrorHelper(error)
            props.setIsSavedState(prevSaved)
            console.error(newError)
        }
            
    }, [props, updateSpotInCache])

    return(
        <div className="flex relative">
            <div className=" absolute hidden">
                <div className="flex flex-col">
                    <span className="uppercase font-semibold">saved to</span>
                    <span className="truncate">{'palcehodler'}</span>
                </div>
                <button className="flex gap-2">
                    <Bookmark/>
                    <span>Change</span>
                </button>
            </div>
            <SpotButtonBase
                title="Save"
                icon={Bookmark}
                data={props.saveCountState}
                color={color}
                onClick={(e) => {
                    e.stopPropagation();
                    onSaveClick(undefined);
                }}
                isActive={props.isSavedState}
                fillColor={fillColor} 
            />
        </div>
    )
}