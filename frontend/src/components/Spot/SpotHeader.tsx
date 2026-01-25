import { Accessibility, Star } from "lucide-react";
import cn from "../../util/tailwind_merger";
import {type JSX } from "react";

type SpotHeaderProps = {
    name: string
    accessibility: boolean
    username: string | undefined
    datePosted: string
    className?: string
    averageRating: number
}

export default function SpotHeader({name, accessibility,
    username, datePosted, className, averageRating}: SpotHeaderProps): JSX.Element{

    const handleDateTime = (): string | undefined => {
        if(!datePosted) return "Invalid date"    
        const localDate = new Date(datePosted)
        const now = new Date()
        const seconds = Math.floor((now.getTime() - localDate.getTime()) / 1000)

        const minute = 60
        const hour = 3600
        const day = 86400
        const week = 604800
        const month = 2592000

        if(seconds < minute){
            return 'Just Now'
        }

        if(seconds < hour){
            const minutes = Math.floor(seconds / minute)
            return `${minutes} ${minutes > 1 ? 'mins' : 'min'} ago`
        }

        if(seconds < day){
            const hours = Math.floor(seconds / hour)
            return `${hours} ${hours > 1 ? 'hours' : 'hour'} ago`
        }

        if(seconds < week){
            const days = Math.floor(seconds / day)
            return `${days} ${days > 1 ? 'days' : 'day'} ago`
        }

        if(seconds < month){
            const weeks = Math.floor(seconds / week)
            return `${weeks} ${weeks > 1 ? 'weeks' : 'week'} ago`
        }

        if(seconds > month){
            return new Intl.DateTimeFormat('en-US', {
                month: 'long',
                day: 'numeric',
                year: 'numeric'
            }).format(localDate)
        }
    }

    return(
        <div className={`${cn("top-1/24 left-1/2 -translate-x-1/2 absolute flex flex-col justify-center items-center gap-[0.25em] border-neutral-300/30 bg-black/10 backdrop-blur-[2px] px-2 py-1 border text-[0.75em] text-white z-20 max-w-[94%] w-full", className)}`}>

            {/* Name & Accessibility */}
            <div className="flex items-center justify-center gap-2 px-2 font-semibold min-w-0 w-full">
                <span className="truncate text-shadow-2xs">{name}</span> 
                {/* TODO: on hover show label saying place is accessible (based on the user who posted) */}
                {accessibility && 
                    <Accessibility 
                        className="w-[1.25em] h-[1.25em] bg-blue-500 p-0.5 rounded-xs shrink-0"
                    />
                }
            </div>
            {<div className="flex justify-center items-center gap-2 text-nowrap max-w-full">

                {/* Rating */}
                <span className="flex items-center gap-0.5 text-white/90 truncate select-none shrink-0 text-[1.2em]">
                    <Star strokeWidth={1} className="w-[1.25em] h-[1.25em]  fill-yellow-400 stroke-yellow-400"/>
                    {averageRating}
                </span>

                {/* Username */}
                {username && 
                <>
                    <span className="select-none">•</span>
                    {/* TODO: on hover show small profile preview of user. on click send to profile */}
                    <div className="text-rose-400 font-medium max-w-[150px] overflow-hidden text-[1em]">
                        <div className="flex">
                            <span 
                                className="truncate"
                            >
                                @{username}
                            </span>
                        </div>
                    </div>
                    
                </>}
                <span className="select-none">•</span>

                {/* Date */}
                <span 
                    className="bg-white/10 px-1 py-0.5 rounded text-[1em] font-medium tracking-wide text-white/90 shadow-sm border border-white/5"
                >
                    {handleDateTime()}
                </span>
            </div>}
        </div>
    )
}