import { Fragment, useCallback, useRef, useState, type CSSProperties, type Dispatch, type JSX, type SetStateAction } from "react";
import ButtonBase from "../../ButtonBase";
import { Star } from "lucide-react";
import { type rateSelectorState, type averageRatingState } from "../Spot";
import { AxiosErrorHelper, protectedInstance } from "../../../../util/axios_api_helpers";
import { useSpotMutation } from "../../../../hooks/SpotHooks/useSpotMutation";
import axios from "axios";

type RateButtonProps = {
    contentId: number
    openRateSelector: boolean
    ratingCount: number
    ratingChoice: number
    onClick?: () => void
    setHoldAverageRating: Dispatch<SetStateAction<averageRatingState>>
    holdAverageRating: number
    setOpenRateSelector: Dispatch<SetStateAction<rateSelectorState>>
}

export default function RateButton(props: RateButtonProps): JSX.Element{
    const [ratingCountHolder, setRatingCountHolder] = useState<number>(props.ratingCount)
    const [isRated, setIsRated] = useState<boolean>(props.ratingChoice ? true : false)
    const [rating, setRating] = useState<number>(props.ratingChoice ? props.ratingChoice : 0)

    const {updateSpotInCache} = useSpotMutation()
    const controllerRef = useRef<AbortController | null>(null)
    const color = "#fbbf24"
    const fillColor = "#fbbf24"

    const onRateClick = useCallback(async(num: number) => {
        const prevRated = isRated
        const prevRateCount = ratingCountHolder
        const prevAverageRating = props.holdAverageRating

        if(controllerRef.current){
            controllerRef.current.abort()
        }

        const controller = new AbortController()
        controllerRef.current = controller

        const range = num > 0 && num <= 5
        const isNotSameRating = num !== rating
        try{
            let response = undefined
            if(range && isNotSameRating){
                const wasRated = isRated

                setIsRated(true)
                if(!prevRated) {
                    setRatingCountHolder(prev => prev + 1)
                }
                response = await protectedInstance.post(`/spot/rate/${props.contentId}`, 
                    {rating_choice: num},
                    {signal: controller.signal}
                )

                if(response.status === 201){
                    const newRating = response.data.rating
                    const newAverage = response.data.new_average
                    const newRatingCount = response.data.new_total_ratings
                    if(!wasRated) setRatingCountHolder(newRatingCount)
                    setRating(newRating)
                    props.setHoldAverageRating(newAverage)
                    props.setOpenRateSelector(false)
                    updateSpotInCache(props.contentId, {
                        rating_choice: newRating,
                        total_num_of_ratings: newRatingCount,
                        average_rating: newAverage
                    })
                }

                
            } else if(num === 0) {
                setIsRated(false)
                if(prevRateCount) {
                    setRatingCountHolder(prev => prev - 1)
                    props.setHoldAverageRating(prev => prev - num)
                }
                response = await protectedInstance.delete(`/spot/rate/${props.contentId}`, {signal: controller.signal})
                 
                if(response.status === 200) {
                    const newAverage = response.data.new_average
                    const newRatingCount = response.data.new_total_ratings
                    setRating(0)
                    setRatingCountHolder(newRatingCount)
                    props.setHoldAverageRating(newAverage)
                    props.setOpenRateSelector(false)
                    updateSpotInCache(props.contentId, {
                        rating_choice: null,
                        total_num_of_ratings: newRatingCount,
                        average_rating: newAverage
                    })
                }  
            } 
        }catch(error){
            const newError = AxiosErrorHelper(error)
            if(axios.isCancel(newError)) return
            props.setHoldAverageRating(prevAverageRating)
            setIsRated(prevRated)
            setRatingCountHolder(prevRateCount)
            console.error(newError)
        } 
    }, [props, updateSpotInCache, isRated, ratingCountHolder, rating])

    const rateButtonHandler = useCallback(() => {
        if(isRated){
            onRateClick(0)
        }else{
            props.setOpenRateSelector((prev) => !prev)
        }
    },[props, onRateClick, isRated])

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
            <ButtonBase
                title="Rate"
                icon={Star}
                data={ratingCountHolder}
                color={color}
                onClick={(e) => {
                    e.stopPropagation()
                    rateButtonHandler()
                }}
                isActive={isRated}
                fillColor={fillColor} 
            />
        </div>
    )
}