import { useCallback, useRef, useState, type JSX} from "react";
import { Bookmark} from "lucide-react";
import ButtonBase from "../../ButtonBase";
import { useSpotMutation } from "../../../../hooks/SpotHooks/useSpotMutation";
import { protectedInstance } from "../../../../util/axiosHelpers";
import axios from "axios";

type SaveButton =  {
    isSaved: boolean
    saveCount: number
    contentId: number
    collections: Array<{is_default: boolean, id: number}>
}

// TODO: add functionality to change saved item to different collection
export default function SaveButton(props: SaveButton): JSX.Element{

    const [isSavedState, setIsSavedState] = useState<boolean>(props.isSaved)
    const [saveCountState, setSaveCountState] = useState<number>(props.saveCount)

    const {updateSpotInCache} = useSpotMutation()
    const controllerRef = useRef<AbortController | null>(null)

    const color = "#60a5fa"
    const fillColor = "#60a5fa"
    
    const onSaveClick = useCallback(async(collectionId: number | undefined) => {
        
        if(props.collections.length === 0) return

        const defaultCollection = props.collections.find((item) => item.is_default === true)
        const prevSaved = isSavedState
        const prevSaveCount = saveCountState

        if(collectionId === undefined && defaultCollection === undefined) return

        if(controllerRef.current){
            controllerRef.current.abort()
        }
        const controller = new AbortController()
        controllerRef.current = controller

        try{
            
            setIsSavedState(!prevSaved)
            setSaveCountState((prev: number) => !prevSaved ? prev + 1: prev - 1)

            const response = await protectedInstance.post(`/collection/${collectionId ? collectionId : defaultCollection && defaultCollection.id}`, 
                {spot_id: props.contentId},
                {signal: controller.signal}
            )

            if(response.status === 200 || response.status === 201){
                const data = response.data
                const isSaved = data.saved
                const newSpotSaveCount = data.spot_save_count
                updateSpotInCache(props.contentId, {
                    save_count: newSpotSaveCount,
                    is_saved: isSaved
                })
            }
        }catch(error){
            if(axios.isCancel(error)) return
            setSaveCountState(prevSaveCount)
            setIsSavedState(prevSaved)
            console.error(error)
        }
            
    }, [props, updateSpotInCache, isSavedState, saveCountState])

    return(
        <div className="flex relative">
            <div className=" absolute hidden">
                <div className="flex flex-col">
                    <span className="uppercase font-semibold">saved to</span>
                    <span className="truncate">{'placehodler'}</span>
                </div>
                <button className="flex gap-2">
                    <Bookmark/>
                    <span>Change</span>
                </button>
            </div>
            <ButtonBase
                title="Save"
                icon={Bookmark}
                data={saveCountState}
                color={color}
                onClick={(e) => {
                    e.stopPropagation();
                    onSaveClick(undefined);
                }}
                isActive={isSavedState}
                fillColor={fillColor} 
            />
        </div>
    )
}