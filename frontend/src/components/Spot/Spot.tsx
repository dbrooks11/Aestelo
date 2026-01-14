import { useState, type JSX} from "react"
import { ChevronLeft, ChevronRight } from "lucide-react"
import SpotTags from "./SpotTags"
import SpotButtons from "./SpotButtons"
import SpotDescripton from "./SpotDesciption"
import SpotHeader from "./SpotHeader"
import SpotPhotoCounter from "./SpotPhotoCount"
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




export default function Spot({spot}): JSX.Element{

    const [progress, setProgress] = useState<number>(1)
    const [total, setTotal ] = useState<number>(spot.total_num_of_photos)
    
    const mediaList = spot.spot_media.sort((a:{sort_order: number}, b:{sort_order: number}) => a.sort_order - b.sort_order)

    // TODO: change username prop in header to users username for header
    return(
        
        <div className="flex flex-col dark:bg-off-slate bg-white mx-auto mb-200 border dark:border-border-dark border-border-light rounded-sm w-90 mt-10">
            
            {/* Images and Header container */}
            <div className="relative flex flex-1">
                
                {/* Header */}
                <SpotHeader
                    name={spot.name}
                    accessibility={spot.accessibility}
                    averageRating={spot.average_rating}
                    username={'chocolate'}
                    datePosted={spot.date_posted}
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
                <SpotDescripton
                    description={spot.description}
                />
                {/* TODO: fix screen snapping when description is toggled */}
                    
                <SpotPhotoCounter
                    progress={progress}
                    total={total}
                />
            
                {/* Photos */}
                <div className="relative aspect-4/5 object-cover flex flex-1">
                    {mediaList.map((item: {photo_path_url: string}, index: number) => {
                        const shouldRender = Math.abs(index - (progress - 1)) <= 1
                        
                        if(!shouldRender) return null

                        return (<img
                            key={index}
                            src={item.photo_path_url}
                            loading={index === progress - 1 ? "eager" : "lazy"} 
                            className={`
                                absolute inset-0 w-full h-full object-cover
                                ${index === progress - 1 ? 'opacity-100 z-10' : 'opacity-0 z-0'}
                            `}
                            alt={`Spot content ${index + 1}`}
                        ></img>)
                    } )}
                </div>
                
            </div>
            {/* Action button and tags container */}
            <div className="flex flex-col dark:bg-off-slate w-full min-h-25">
                <SpotTags
                    tags={spot.hashtags}
                />
                <SpotButtons
                    shareCount={spot.share_count}
                    saveCount={spot.save_count}
                    totalNumOfRatings={spot.total_num_of_ratings}
                    visitCount={spot.visit_count}
                />   
            </div>
        </div>
    )
}