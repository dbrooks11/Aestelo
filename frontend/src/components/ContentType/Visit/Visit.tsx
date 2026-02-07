import { useMemo, useState, type JSX } from "react";
import {type ButtonType } from "../PostTypeActionButtons";
import ContentContainerBase from "../ContentContainerBase";
import VisitHeader from "./VisitHeader";
import DescriptonOrCaption from "../ContentDesciptionOrCaption";
import PhotoCounter from "../PhotoCounter";
import Photos from "../Photos";
import Tags from "../ContentTags";
import PostTypeActionButtons from "../PostTypeActionButtons";
import { ExternalLink } from "lucide-react";


export default function Visit({visit}): JSX.Element{
    const [progress, setProgress] = useState<number>(1)

    const visitButtons: Array<ButtonType> = useMemo(() => 
    [
        {
            order: 1,
            position: 'left',
            title: 'Share',
            icon: ExternalLink,
            color: '#c084fc',
            fillColor: '#c084fc',
            data: visit.share_count
        },
        {
            order: 2,
            position: 'left',
            component: (
                <SaveButton 
                    spotId={spot.id}
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
                    spotId={spot.id}
                    openRateSelector={openRateSelector}
                    ratingChoice={spot.rating_choice}
                    ratingCount={spot.total_num_of_ratings}
                    setHoldAverageRating={setHoldAverageRating}
                    holdAverageRating={holdAverageRating}
                    setOpenRateSelector={setOpenRateSelector}
                />
            )
        },
    ], [visit.share_count]) 
    
    
    return(
        <ContentContainerBase
            props={{
                progress: progress,
                setProgress: setProgress
            }}
        >
            {/* Child 1 */}
            <>
                <VisitHeader
                    username={''}
                />
                <DescriptonOrCaption
                    description={''}
                />
                <PhotoCounter
                    progress={progress}
                    total={0}
                />
                <Photos
                    media={''}
                    progress={progress}
                    onClickFunctionality={''}
                />

            </>

            {/* Child 2 */}
            <>
                <Tags
                    tags={['']}
                />
                <PostTypeActionButtons
                    buttons={visitButtons}
                />
            </>
        </ContentContainerBase>
    )
}