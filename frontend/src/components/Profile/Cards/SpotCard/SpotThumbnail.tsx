import {type JSX } from "react";



export default function SpotThumbnail({spot}): JSX.Element{

    const thumbnail = [...spot.media].find((photo) => photo.sort_order === 1)
    
    return(
        <div className="relative aspect-4/5 object-cover flex flex-1 select-none">
            <img
                src={thumbnail?.photo_path_url}
                loading="lazy"
                className="w-full h-full object-cover"
                alt={`Spot ${spot.id} Thumbnail`}
            ></img>
        </div>
    )
}