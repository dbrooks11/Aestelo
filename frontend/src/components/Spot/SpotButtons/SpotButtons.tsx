import { useMemo, useState, type ComponentType, type JSX, 
    type SVGProps, type Dispatch, type SetStateAction,
    type ReactNode,
    Fragment} from "react";
import {ExternalLink, type LucideProps} from "lucide-react"
import VIconRounded from "../../DynamicSvgs/VIconRounded"
import SaveButton from "./SaveButton";
import RateButton from "./RateButton";
import SpotButtonBase from "./SpotButtonBase";


type IconComponent = ComponentType<LucideProps | SVGProps<SVGSVGElement>>;

export type SpotButtonType = {
    order: number
    title?: string
    position: 'left' | 'right'
    color?: string
    fillColor?: string
    icon?: IconComponent
    data?: number
    component?: ReactNode 
    /* eslint-disable @typescript-eslint/no-explicit-any */
    handler?: (value: any) => any 
}

type Collection = {
    name: string
    id: number,
    is_default:boolean
}

type SpotButtonProps = {
    shareCount: number,
    saveCount: number,
    ratingCount: number
    visitCount: number
    spotId: number
    ratingChoice: number
    openRateSelector: boolean
    setOpenRateSelector: Dispatch<SetStateAction<boolean>>
    setHoldAverageRating: Dispatch<SetStateAction<number>>
    hasVisited: boolean,
    isSaved: boolean,
    collections: Array<Collection>
}

export default function SpotButtons({shareCount, saveCount, 
    ratingCount, visitCount, spotId, ratingChoice, openRateSelector, setOpenRateSelector,
    setHoldAverageRating, hasVisited, isSaved, collections
}: SpotButtonProps): JSX.Element{

    const [ratingCountHolder, setRatingCountHolder] = useState<number>(ratingCount)
    const [isRated, setIsRated] = useState<boolean>(ratingChoice ? true : false)
    const [rating, setRating] = useState<number>(ratingChoice ? ratingChoice : 0)
    const [isSavedState, setIsSavedState] = useState<boolean>(isSaved)
    // const [hasVisitedState, setHasVisitedState] = useState<boolean>(hasVisited)
    const [saveCountState, setSaveCountState] = useState<number>(saveCount)    


    const spotButtons: Array<SpotButtonType> = useMemo(() => 
    [
        {
            order: 1,
            position: 'left',
            title: 'Share',
            icon: ExternalLink,
            color: '#c084fc',
            fillColor: '#c084fc',
            data: shareCount,
            handler: () => console.log("Share logic here")
        },
        {
            order: 2,
            position: 'left',
            component: (
                <SaveButton 
                    spotId={spotId}
                    isSavedState={isSavedState}
                    saveCountState={saveCountState}
                    setSaveCountState={setSaveCountState}
                    setIsSavedState={setIsSavedState} 
                    collections={collections}
                />
            )
        },
        {
            order: 3,
            position: 'left',
            component: (
                <RateButton 
                    rating={rating}
                    ratingCountHolder={ratingCountHolder}
                    spotId={spotId}
                    openRateSelector={openRateSelector}
                    isRated={isRated}
                    setIsRated={setIsRated}
                    setRatingCountHolder={setRatingCountHolder}
                    setRating={setRating}
                    setHoldAverageRating={setHoldAverageRating}
                    setOpenRateSelector={setOpenRateSelector}
                    
                />
            )
        },
        {
            order: 4,
            position: 'right',
            title: 'Visit',
            icon: VIconRounded,
            color: '#22c55e',
            fillColor: '#22c55e',
            data: visitCount,
            handler: () => console.log("Visit logic here")
        },
    ], [shareCount, ratingCountHolder, visitCount, saveCountState, rating, openRateSelector,
    collections, isSavedState, spotId, isRated, setHoldAverageRating, setOpenRateSelector])    

    const {leftButtons, rightButtons} = useMemo(() => {
        const sortedButtons = [...spotButtons].sort((btn1, btn2) => btn1.order - btn2.order)
        return{
            leftButtons: sortedButtons.filter(btn => btn.position === 'left'),
            rightButtons: sortedButtons.filter(btn => btn.position === 'right')
        }
    }, [spotButtons])

    function renderSpotButtons(btnArray: Array<SpotButtonType>): JSX.Element {
        return(
            <>
                <div className="flex gap-2.5 text-neutral-600 dark:text-neutral-400 items-center">
                {btnArray.map((btn, index) => {
                    if (btn.component) {
                        return <Fragment key={index}>{btn.component}</Fragment>
                    }
                    return (
                        <SpotButtonBase
                            key={index}
                            title={btn.title!}
                            icon={btn.icon}
                            data={btn.data!}
                            fillColor={btn.fillColor}
                            color={btn.color!}
                            onClick={btn.handler}
                        />
                    );
                })}
            </div>
            </>
        )
    }

    return(
        <div className="flex flex-1 justify-between items-center gap-4 px-4 w-full text-xs">
            {renderSpotButtons(leftButtons)}
            {renderSpotButtons(rightButtons)}
        </div>
    )
}