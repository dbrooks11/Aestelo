import { type JSX } from "react";
import { Accessibility, GalleryVerticalEnd } from "lucide-react";
import cn from "../../../../util/tailwind_merger";
import SpotHeader from "../../../Spot/SpotHeader";
import SpotDescripton from "../../../Spot/SpotDesciption";
import SpotThumbnail from "./SpotThumbnail";

export default function SpotCard({spot, className, onClick, includeUsername}): JSX.Element{
    
    return(
        <div 
            className={`${cn('flex flex-col dark:bg-off-slate bg-white border dark:border-border-dark border-border-light rounded-sm text-sm lg:text-base', className)}`}
            onClick={onClick}
        >
            <div className="relative flex flex-1">
                
            {/* Header */}
            <SpotHeader
                name={spot.name}
                accessibility={spot.accessibility}
                datePosted={spot.date_posted}
                username={includeUsername ? spot.username : undefined}
                averageRating={spot.average_rating}
                className="hidden lg:flex"
            />

            {spot.description && <SpotDescripton
                description={spot.description}
                className="hidden lg:flex"
            />}

            {/* Photos */}
            <SpotThumbnail
                spot={spot}
            />

            {spot.media.length > 1 && <GalleryVerticalEnd
                className="absolute bottom-0 right-1  md:bottom-2 md:right-2 z-10 stroke-white w-[1.25em] lg:w-[1.5em]"
                strokeWidth={1.5}
            />}

            {spot.accessibility &&
                <Accessibility 
                    className="w-[1em] h-[1em] sm:w-[1.25em] sm:h-[1.25em] bg-blue-500/80 p-0.5 rounded-xs shrink-0 absolute lg:hidden top-1 left-1 z-10 text-white/70"
                />
            }
            </div>
        </div>
    )
}