import { type JSX} from "react"
import testImage from "../../assets/testImage.jpg"
import whitePlain from "../../assets/white_plain.jpg"
import PostTags from "./PostTags"
import PostButtons from "./PostButtons"
import PostDescripton from "./PostDesciption"
import PostHeader from "./PostHeader"
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


    //TODO: move containerRef and useEffect to tags component 
    

    

    const showPhotos = (photos: Array<object>): JSX.Element => {

        return(
            <></>
        )
    }

    return(
        
        <div className="flex flex-col dark:bg-off-slate mx-auto mb-200 border border-border-dark rounded-sm w-90">
            
            {/* Images and Header container */}
            <div className="relative flex flex-1">
                
                {/* Header */}
                <PostHeader/>

                {/* Description and Photo Counter */}
                <PostDescripton/>
                {/* TODO: fix screen snapping when description is toggled */}
                    
                <div 
                    className="right-1 bottom-1 absolute flex justify-center items-center p-1 border border-white rounded-full w-8 h-8 text-[10px] text-white">
                    <span>3/10</span>
                </div>
            
                {/* Photos */}
                <img 
                    src={testImage} 
                    className="w-full h-full"
                    alt='Post content'
                ></img>
            </div>
            {/* Action button and tags container */}
            <div className="flex flex-col bg-off-slate backdrop-blur-md w-full min-h-25">
                <PostTags/>
                <PostButtons/>   
            </div>
        </div>
    )
}