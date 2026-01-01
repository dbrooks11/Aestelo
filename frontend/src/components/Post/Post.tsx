import { useState, type JSX} from "react"
import { ChevronLeft, ChevronRight } from "lucide-react"
import testImage from "../../assets/testImage.jpg"
import whitePlain from "../../assets/white_plain.jpg"
import blackPlain from "../../assets/black_plain.jpg"
import testImage2 from "../../assets/testImage2.jpg"
import PostTags from "./PostTags"
import PostButtons from "./PostButtons"
import PostDescripton from "./PostDesciption"
import PostHeader from "./PostHeader"
import PostPhotoCounter from "./PostPhotoCount"
// type PostProps = {
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

export default function Post(): JSX.Element{

    const [progress, setProgress] = useState<number>(5)
    const [total, setTotal ] = useState<number>(10)
    

    

    const showPhotos = (photos: Array<object>): JSX.Element => {

        return(
            <></>
        )
    }

    return(
        
        <div className="flex flex-col dark:bg-off-slate bg-white mx-auto mb-200 border dark:border-border-dark border-border-light rounded-sm w-90 mt-10">
            
            {/* Images and Header container */}
            <div className="relative flex flex-1">
                
                {/* Header */}
                <PostHeader/>

                {/* Arrow Buttons */}
                <div 
                    className="absolute flex left-1 bottom-[50%]">
                    <button 
                        className=" w-7 h-7 flex items-center justify-center rounded-full bg-black/10 backdrop-blur-[2px] text-white/70 border border-white/10  active:scale-90 cursor-pointer shadow-2xl" 
                        onClick={() => setProgress(Math.max(1, progress - 1))}
                        aria-label="previous button"
                    >
                        <ChevronLeft/>
                    </button>
                </div>
                <div className="absolute flex right-1 bottom-[50%]">
                    <button 
                        className=" w-7 h-7 flex items-center justify-center rounded-full bg-black/10 backdrop-blur-[2px] text-white/70 border border-white/10  active:scale-90 cursor-pointer" 
                        onClick={() => setProgress(Math.min(total, progress + 1))}
                        aria-label="next button"
                    >
                        <ChevronRight/>
                    </button>
                </div>
                

                {/* Description and Photo Counter */}
                <PostDescripton/>
                {/* TODO: fix screen snapping when description is toggled */}
                    
                <PostPhotoCounter
                    progress={progress}
                    total={total}
                />
            
                {/* Photos */}
                <div>
                    <img 
                        src={testImage2} 
                        className="w-full h-full"
                        alt='Post content'
                    ></img>
                </div>
                
            </div>
            {/* Action button and tags container */}
            <div className="flex flex-col dark:bg-off-slate w-full min-h-25">
                <PostTags/>
                <PostButtons/>   
            </div>
        </div>
    )
}