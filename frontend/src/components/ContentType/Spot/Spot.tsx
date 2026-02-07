import { useMemo, useState, type JSX} from "react"
import { ExternalLink } from "lucide-react"
import VIconRounded from "../../DynamicSvgs/VIconRounded"
import SaveButton from "./SpotButtons/SaveButton"
import RateButton from "./SpotButtons/RateButton"
import ContentContainerBase from "../ContentContainerBase"
import Tags from "../ContentTags"
import PostTypeActionButtons from "../PostTypeActionButtons"
import DescriptonOrCaption from "../ContentDesciptionOrCaption"
import SpotHeader from "./SpotHeader"
import PhotoCounter from "../PhotoCounter"
import Photos from "../Photos"
import { type ButtonType } from "../PostTypeActionButtons"

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

export type rateSelectorState = boolean
export type averageRatingState = number


export default function Spot({spot, collections,  className}): JSX.Element{

    
    const [progress, setProgress] = useState<number>(1)
    const [openRateSelector, setOpenRateSelector] = useState<boolean>(false)
    const [holdAverageRating, setHoldAverageRating] = useState<number>(spot.average_rating)

    const spotButtons: Array<ButtonType> = useMemo(() => 
    [
        {
            order: 1,
            position: 'left',
            title: 'Share',
            icon: ExternalLink,
            color: '#c084fc',
            fillColor: '#c084fc',
            data: spot.share_count
        },
        {
            order: 2,
            position: 'left',
            component: (
                <SaveButton 
                    contentId={spot.id}
                    collections={collections}
                    isSaved={spot.is_saved}
                    saveCount={spot.save_count}
                />
            )
        },
        {
            order: 3,
            position: 'left',
            component: (
                <RateButton 
                    contentId={spot.id}
                    openRateSelector={openRateSelector}
                    ratingChoice={spot.rating_choice}
                    ratingCount={spot.total_num_of_ratings}
                    setHoldAverageRating={setHoldAverageRating}
                    holdAverageRating={holdAverageRating}
                    setOpenRateSelector={setOpenRateSelector}
                />
            )
        },
        {
            order: 4,
            position: 'right',
            title: 'Visit',
            icon: VIconRounded,
            color: '#22c55e',
            fillColor: '#22c55e',
            data: spot.visit_count
        },
    ], [openRateSelector, collections, setHoldAverageRating, setOpenRateSelector, holdAverageRating, spot.id, spot.is_saved, spot.rating_choice, spot.save_count, spot.share_count, spot.total_num_of_ratings,spot.visit_count])    

    return(
        
        <ContentContainerBase
            props = {{
                progress: progress,
                setProgress: setProgress,
                totalNumOfPhotos: spot.total_num_of_photos,
                className: className
            }}
        >
            {/* Child 1 ( TOP HALF)*/}
            <>
                {/* Header */}
                <SpotHeader
                    name={spot.name}
                    accessibility={spot.accessibility}
                    username={spot.username}
                    datePosted={spot.date_posted}
                    averageRating={holdAverageRating}
                />

                {/* Description and Photo Counter */}
                {spot.description && <DescriptonOrCaption
                    description={spot.description}
                />}
                    
                <PhotoCounter
                    progress={progress}
                    total={spot.total_num_of_photos}
                />
            
                {/* Photos */}
                <Photos
                    media={spot.media}
                    progress={progress}
                    onClickFunctionality={setOpenRateSelector}
                />
                
            </>
            {/* Child 2 (BOTTOM HALF)*/}
            <>
                <Tags
                    tags={spot.hashtags}
                />
                <PostTypeActionButtons
                    buttons={spotButtons}  
                />   
            </>
        </ContentContainerBase>
    )
}