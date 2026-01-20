import { useState, type JSX} from "react"
import { ChevronLeft, ChevronRight } from "lucide-react"
import cn from "../../util/tailwind_merger"
import SpotTags from "./SpotTags"
import SpotButtons from "./SpotButtons"
import SpotDescripton from "./SpotDesciption"
import SpotHeader from "./SpotHeader"
import SpotPhotoCounter from "./SpotPhotoCount"
import SpotPhoto from "./SpotPhoto"

// type SpotProps = {
//     name: string
//     date_posted: string
//     description: string
//     total_num_of_photos: number
//     average_rating: number
//     total_num_of_ratings: string
//     save_count: number
//     share_count: string
//     hashtags: Array<string>
//     accessibility: boolean

// }


export default function Spot({spot, className}): JSX.Element{

    const [progress, setProgress] = useState<number>(1)
    const [total, setTotal ] = useState<number>(spot.total_num_of_photos)
    const [ openRateSelector, setOpenRateSelector] = useState<boolean>(false)
    const [holdAverageRating, setHoldAverageRating] = useState<number>(spot.average_rating)
    // TODO: change username prop in header to users username for header
    return(
        
        <div 
            className={`${cn('flex flex-col dark:bg-off-slate bg-white border dark:border-border-dark border-border-light rounded-sm w-90', className)}`}
        >
            
            {/* Images and Header container */}
            <div 
                className="relative flex flex-1"
            >
                
                {/* Header */}
                <SpotHeader
                    name={spot.name}
                    accessibility={spot.accessibility}
                    username={spot.username}
                    datePosted={spot.date_posted}
                    holdAverageRating={holdAverageRating}
                />

                {/* Arrow Buttons */}
                <div 
                    className="absolute flex left-1 bottom-[50%]">
                    <button 
                        className=" w-7 h-7 flex items-center justify-center rounded-full bg-black/10 backdrop-blur-[2px] text-white/70 border border-white/10  active:scale-90 cursor-pointer shadow-2xl z-20" 
                        onClick={() => setProgress(Math.max(1, progress - 1))}
                        aria-label="previous button"
                    >
                        <ChevronLeft/>
                    </button>
                </div>
                <div className="absolute flex right-1 bottom-[50%]">
                    <button 
                        className=" w-7 h-7 flex items-center justify-center rounded-full bg-black/10 backdrop-blur-[2px] text-white/70 border border-white/10  active:scale-90 cursor-pointer z-20" 
                        onClick={() => setProgress(Math.min(total, progress + 1))}
                        aria-label="next button"
                    >
                        <ChevronRight/>
                    </button>
                </div>
                

                {/* Description and Photo Counter */}
                {spot.description && <SpotDescripton
                    description={spot.description}
                />}
                {/* TODO: fix screen snapping when description is toggled */}
                    
                <SpotPhotoCounter
                    progress={progress}
                    total={total}
                />
            
                {/* Photos */}
                <SpotPhoto
                    spot={spot}
                    progress={progress}
                    setOpenRateSelector={setOpenRateSelector}
                />
                
            </div>
            {/* Action button and tags container */}
            <div className="flex flex-col dark:bg-off-slate w-full min-h-25">
                <SpotTags
                    tags={spot.hashtags}
                />
                <SpotButtons
                    shareCount={spot.share_count}
                    saveCount={spot.save_count}
                    ratingCount={spot.total_num_of_ratings}
                    visitCount={spot.visit_count}
                    spotId={spot.id}
                    ratingChoice={spot.rating_choice}
                    openRateSelector={openRateSelector}
                    setOpenRateSelector={setOpenRateSelector}
                    setHoldAverageRating={setHoldAverageRating}
                />   
            </div>
        </div>
    )
}