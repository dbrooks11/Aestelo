import { type JSX } from "react";
import { Accessibility, Star, Ellipsis
    ,ExternalLink, Bookmark} from "lucide-react";
import VIconRounded from "../DynamicSvgs/VIconRounded";

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
    return(
        
        <div className="flex flex-col border border-white w-80 h-120">
            {/* Images and Header container */}
            <div className="relative h-full w-full">
                
                {/* Header */}
                <div className="flex flex-col items-center justify-center border border-white absolute right-15 top-4 bg-white/10 backdrop-blur-lg py-1 px-2">
                    <div className="flex gap-2">
                        <span>Name placeholder</span>
                        <Accessibility/>
                    </div>
                    <div className="flex gap-2 items-center justify-center">
                        <span className="flex"><Star strokeWidth={1}/>4.8</span>
                        <span>•</span>
                        <span>5.2k</span>
                        <span>•</span>
                        <span>2 mins ago</span>
                    </div>
                </div>

                {/* Description and Photo Counter */}
                    <div className="flex text-white absolute bottom-1 left-1">
                        <span aria-hidden='true'>[</span>
                        <span aria-hidden='true' className="pt-0.5"><Ellipsis/></span>
                        <span aria-hidden='true'>]</span>
                    </div>

                    <div className="border w-8 h-8 border-white rounded-full p-1 text-[10px] text-white absolute bottom-1 right-1 flex items-center justify-center">
                        <span>3/10</span>
                    </div>
                
                {/* Photos */}
                <img></img>
                <img></img>
            </div>
            {/* Action button and tags container */}
            <div className="border border-white w-full h-30">

                {/* Hashtags */}
                {/* TODO: map over each tag to display it */}
                <div className="text-white">
                    <span>Tag1</span>
                    <span>Tag1</span>
                    <span>Tag1</span>
                    <span>Tag1</span>
                    <span>Tag1</span>
                    <span>Tag1</span>
                </div>      
                <div className="flex text-white gap-6 items-center justify-center">
                    <div className="flex flex-col">
                        <button><ExternalLink/></button>
                        <span>400</span>
                    </div>
                    <div className="flex flex-col">
                        <button><Bookmark/></button>
                        <span>1k</span>
                    </div>
                    <div className="flex flex-col">
                        <button><Star/></button>
                        <span>145k</span>
                    </div>
                    <div className="flex flex-col">
                        <button><VIconRounded/></button>
                        <span>234</span>
                    </div>
                </div>          
            </div>
        </div>
    )
}