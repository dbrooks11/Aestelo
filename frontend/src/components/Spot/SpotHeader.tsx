import { Accessibility, Star } from "lucide-react";
import { type JSX } from "react";

type SpotHeaderProps = {
    name: string
    accessibility: boolean
    averageRating: number
    username: string
    datePosted: string
}

export default function SpotHeader({name, accessibility,averageRating,
    username, datePosted}: SpotHeaderProps): JSX.Element{
    
    const localDate = new Date(datePosted + 'Z').toLocaleString()

    // TODO: show date from users local time (2mins ago, 4 hours ago, etc)
    const handleDateTime = () => {
       const localDate = new Date(datePosted + 'Z').toLocaleString() 
       const now = new Date()
    }

    return(
        <div className="top-4 left-[50%] -translate-x-1/2 absolute flex flex-col justify-center items-center gap-1 
        border-neutral-300/30 bg-black/10 backdrop-blur-[2px] px-2 py-1 border text-xs text-white z-20">
            <div className="flex items-center gap-2 px-2 font-semibold text-nowrap">
                {/* TODO: max char for name 40 characters */}
                <span>{name}</span> 
                {/* TODO: on hover show label saying place is accessible (based on the user who posted) */}
                {accessibility && 
                    <Accessibility 
                        className="w-4 h-4 bg-blue-500 p-0.5 rounded-xs"
                    />
                }
            </div>
            <div className="flex justify-center items-center gap-2 text-nowrap">
                <span className="flex items-center gap-0.5 text-white/90"><Star strokeWidth={1} className="w-5 h-5 fill-yellow-400 stroke-yellow-400"/>{averageRating}</span>
                <span>•</span>
                {/* TODO: on hover show small profile preview of user. on click send to profile */}
                <span className="text-rose-400 font-medium">{username}</span>
                <span>•</span>
                {/* on hover, show full data posted */}
                <span className="text-white/90">{localDate}</span>
            </div>
        </div>
    )
}