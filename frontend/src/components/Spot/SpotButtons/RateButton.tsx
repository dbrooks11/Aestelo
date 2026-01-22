import { Fragment, useCallback, type CSSProperties, type Dispatch, type JSX, type SetStateAction } from "react";
import SpotButtonBase from "./SpotButtonBase";
import { Star } from "lucide-react";
import { AxiosErrorHelper, protectedInstance } from "../../../util/axios_api_helpers";
import { useSpotMutation } from "../../../hooks/SpotHooks/useSpotMutation";

type RateButtonProps = {
    rating: number
    spotId: number
    openRateSelector: boolean
    onClick?: () => void
    setRating: Dispatch<SetStateAction<number>>
    setHoldAverageRating: Dispatch<SetStateAction<number>>
    setIsRated: Dispatch<SetStateAction<boolean>>
    isRated: boolean
    setRatingCountHolder: Dispatch<SetStateAction<number>>
    setOpenRateSelector: Dispatch<SetStateAction<boolean>>
    ratingCountHolder: number
}

export default function RateButton(props: RateButtonProps): JSX.Element{

    const {updateSpotInCache} = useSpotMutation()
    const color = "#fbbf24"
    const fillColor = "#fbbf24"

    const onRateClick = useCallback(async(num: number) => {
        const prevRated = props.isRated
        const prevRateCount = props.ratingCountHolder
        try{
            let response = undefined
            if(num > 0 && num <= 5){
                const wasRated = props.isRated
                
                props.setIsRated(true)
                if(!prevRated) props.setRatingCountHolder(prev => prev + 1)
                response = await protectedInstance.post(`/spot/rate/${props.spotId}`, {
                    rating_choice: num
                })

                if(response.status === 201){
                    const newRating = response.data.rating
                    const newAverage = response.data.new_average
                    const newRatingCount = response.data.new_total_ratings
                    if(!wasRated) props.setRatingCountHolder(newRatingCount)
                    props.setRating(newRating)
                    props.setHoldAverageRating(newAverage)
                    props.setOpenRateSelector(false)
                    updateSpotInCache(props.spotId, {
                        rating_choice: newRating,
                        total_num_of_ratings: newRatingCount,
                        average_rating: newAverage
                    })
                }
                
            } else if(num === 0) {
                props.setIsRated(false)
                if(prevRateCount) props.setRatingCountHolder(prev => prev - 1)
                response = await protectedInstance.delete(`/spot/rate/${props.spotId}`)
                 
                if(response.status === 200) {
                    const newAverage = response.data.new_average
                    const newRatingCount = response.data.new_total_ratings
                    props.setRating(0)
                    props.setRatingCountHolder(newRatingCount)
                    props.setHoldAverageRating(newAverage)
                    props.setOpenRateSelector(false)
                    updateSpotInCache(props.spotId, {
                        rating_choice: null,
                        total_num_of_ratings: newRatingCount,
                        average_rating: newAverage
                    })
                }  
            } 
        }catch(error){
            props.setIsRated(prevRated)
            props.setRatingCountHolder(prevRateCount)
            const newError = AxiosErrorHelper(error)
            console.error(newError)
        } 
    }, [props, updateSpotInCache])

    const rateButtonHandler = useCallback(() => {
        if(props.isRated){
            onRateClick(0)
        }else{
            props.setOpenRateSelector((prev) => !prev)
        }
    },[props, onRateClick])

    return (
        <div 
            className="relative flex group"
            style={{ '--btn-color': color, '--btn-fill-color': fillColor } as CSSProperties}
        >
            {props.openRateSelector && <div className="-top-16 left-[50%] absolute flex flex-row-reverse justify-center items-center dark:bg-off-slate border dark:border-neutral-700 rounded-xs p-2 -translate-x-1/2 shadow-lg z-20 hover:dark:text-white/80">
                {[5,4,3,2,1].map((num) => {
                    return (
                        <Fragment key={num}>
                            <input 
                                type="radio"
                                name="rating"
                                id={`${num}`}
                                defaultChecked={props.rating === num}
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
                                <Star
                                    strokeWidth={1}
                                    className={`stroke-current fill-inherit w-8 h-8`}
                                >
                                </Star>
                            </label>
                        </Fragment> 
                    )
                })}
                <div
                    className="-bottom-1.5 absolute dark:bg-off-slate border-neutral-700 border-r border-b w-3 h-3 rotate-45"
                    aria-hidden
                ></div>
            </div>}
            <SpotButtonBase
                title="Rate"
                icon={Star}
                data={props.ratingCountHolder}
                color={color}
                onClick={(e) => {
                    e.stopPropagation()
                    rateButtonHandler()
                }}
                isActive={props.isRated}
                fillColor={fillColor} 
            />
        </div>
    )
}