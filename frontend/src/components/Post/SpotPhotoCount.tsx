import { type JSX } from "react";
import { CircularProgress } from "../CircularProgressBar";

type SpotPhotoCounterProps = {
    progress: number
    total: number

}

export default function SpotPhotoCounter({progress, total}: SpotPhotoCounterProps): JSX.Element{
    

    return(
        <div 
            className="right-1 bottom-2 absolute"
            >
            <CircularProgress
                current={progress}
                total={total}
                size={30}
                strokeWidth={2}
                color={progress === total ? 'text-green-500' : 'text-white'}
            />
        </div>
    )
}