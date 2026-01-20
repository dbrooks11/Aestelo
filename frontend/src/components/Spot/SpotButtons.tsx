import { useMemo, useState, type CSSProperties, type ComponentType, type JSX, 
    type SVGProps, Fragment, type Dispatch, type SetStateAction, useCallback} from "react";
import { Star,ExternalLink, Bookmark, type LucideProps} from "lucide-react"
import VIconRounded from "../DynamicSvgs/VIconRounded"
import { handleNumStats } from "../../util/StatConverter";
import { AxiosErrorHelper, protectedInstance } from "../../util/axios_api_helpers";
import { useSpotMutation } from "../../hooks/SpotHooks/useSpotMutation";


type IconComponent = ComponentType<LucideProps | SVGProps<SVGSVGElement>>;

type SpotButtonType = {
    order: number
    title: string
    position: 'left' | 'right'
    color: string
    fillColor?: string
    icon: IconComponent
    data: number
    handler?: (value: unknown) => void //TODO: remove from being optional when done
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
}

export default function SpotButtons({shareCount, saveCount, 
    ratingCount, visitCount, spotId, ratingChoice, openRateSelector, setOpenRateSelector,
    setHoldAverageRating
}: SpotButtonProps): JSX.Element{

    const [ratingCountHolder, setRatingCountHolder] = useState<number>(ratingCount)
    const [isRated, setIsRated] = useState<boolean>(ratingChoice ? true : false)
    const [rating, setRating] = useState<number>(ratingChoice ? ratingChoice : 0)

    const {updateSpotInCache} = useSpotMutation()

    const onRateClick = useCallback(async(num: number) => {
        const prevRated = isRated
        try{
            let response = undefined
            if(num > 0 && num <= 5){
                const wasRated = isRated
                
                setIsRated(true)
                response = await protectedInstance.post(`/spot/rate/${39}`, {
                    rating_choice: num
                })

                if(response.status === 201){
                    const newRating = response.data.rating
                    const newAverage = response.data.new_average
                    const newRatingCount = response.data.new_total_ratings
                    if(!wasRated) setRatingCountHolder(newRatingCount)
                    setRating(newRating)
                    setHoldAverageRating(newAverage)
                    setOpenRateSelector(false)
                    updateSpotInCache(spotId, {
                        rating_choice: newRating,
                        total_num_of_ratings: newRatingCount,
                        average_rating: newAverage
                    })
                }
                
            } else if(num === 0) {
                setIsRated(false)
                response = await protectedInstance.delete(`/spot/rate/${spotId}`)
                 
                if(response.status === 200) {
                    const newAverage = response.data.new_average
                    const newRatingCount = response.data.new_total_ratings
                    setRating(0)
                    setRatingCountHolder(newRatingCount)
                    setHoldAverageRating(newAverage)
                    setOpenRateSelector(false)
                    updateSpotInCache(spotId, {
                        rating_choice: null,
                        total_num_of_ratings: newRatingCount,
                        average_rating: newAverage
                    })
                }  
            } 
        }catch(error){
            setIsRated(prevRated)
            const newError = AxiosErrorHelper(error)
            console.error(newError)
        } 
    }, [isRated, setOpenRateSelector, spotId, updateSpotInCache, setHoldAverageRating])

    const rateButtonHandler = useCallback(() => {
        if(isRated){
            onRateClick(0)
        }else{
            setOpenRateSelector((prev) => !prev)
        }
    },[isRated, setOpenRateSelector, onRateClick]) 


    const spotButtons: Array<SpotButtonType> = useMemo(() => 
    [
        {
            order: 1,
            title: 'Share',
            position: 'left',
            icon: ExternalLink,
            color: '#c084fc',
            data: shareCount
        },
        {
            order: 2,
            title: 'Save',
            position: 'left',
            color: '#60a5fa',
            // fillColor: '#60a5fa',
            icon: Bookmark,
            data: saveCount
        },
        {
            order: 3,
            title: 'Rate',
            color: '#fbbf24',
            fillColor: '#facc15',
            position: 'left',
            icon: Star,
            data: ratingCountHolder,
            handler: rateButtonHandler
        },
        {
            order: 4,
            title: 'Visit',
            color: '#22c55e',
            // fillColor: '#22c55e',
            position: 'right',
            icon: VIconRounded,
            data: visitCount
        },
    ], [shareCount, saveCount, ratingCountHolder, visitCount, rateButtonHandler])    

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
                <div className="flex gap-2.5 text-neutral-600 dark:text-neutral-400">
                    {btnArray.map((btn: SpotButtonType) => {
                            return(
                                <button
                                    key={btn.title}
                                    title={btn.title}
                                    style={{'--btn-color': btn.color, '--btn-fill-color': btn.fillColor} as CSSProperties}
                                    onClick={btn?.handler}
                                    className="group relative flex items-center gap-1 hover:dark:text-white hover:text-black transition-colors cursor-pointer"
                                >
                                    {/* TODO: change stroke and fill to be on when user completes action */}
                                    <btn.icon
                                        strokeWidth={1}
                                        className={`group-hover:stroke-(--btn-color) 
                                            ${(btn.fillColor && isRated && btn.title === 'Rate') && 'fill-(--btn-fill-color) stroke-(--btn-color)'} 
                                            transition-colors `}
                                    >
                                    </btn.icon>
                                    <span className="font-medium text-xs">{handleNumStats(btn.data)}</span>
                                    {(btn.title === 'Rate' && openRateSelector) && <div className="-top-12 left-[50%] absolute flex flex-row-reverse justify-center items-center dark:bg-off-slate px-2 border dark:border-neutral-700 rounded-xs h-10 -translate-x-1/2">
                                        {[5,4,3,2,1].map((num) => {
                                            
                                            return (
                                                <Fragment key={num}>
                                                    <input 
                                                        type="radio"
                                                        name="rating"
                                                        id={`${num}`}
                                                        defaultChecked={rating === num}
                                                        className="hidden peer"
                                                        value={num}
                                                    ></input>
                                                    <label 
                                                        htmlFor={`${num}`}
                                                        onClick={(e) => {
                                                            e.preventDefault()
                                                            e.stopPropagation()
                                                            onRateClick(num)
                                                        }}
                                                        className="hover:fill-(--btn-color) hover:text-(--btn-color) peer-hover:fill-(--btn-color) peer-hover:text-(--btn-color) peer-checked:fill-(--btn-color) peer-checked:text-(--btn-color) transition-colors cursor-pointer fill-transparent"
                                                    >
                                                        <btn.icon
                                                            strokeWidth={1}
                                                            className={`stroke-current fill-inherit`}
                                                        >
                                                        </btn.icon>
                                                    </label>
                                                </Fragment> 
                                            )
                                        })}
                                        <div
                                            className="-bottom-1.5 absolute dark:bg-off-slate border-neutral-700 border-r border-b w-3 h-3 rotate-45"
                                            aria-hidden
                                        ></div>
                                    </div>}
                                </button>
                            )
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