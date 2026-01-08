import { Camera } from "lucide-react";
import { type JSX } from "react";
import { type StepState, type UploadedPhotosState, type PreviewPhotosState } from "../CreateSpotForm";
import { fileCompressionForPreview } from "../../../../util/client_image_compression";

export type Step1 = {
    setStep: (num: StepState) => void
    setUploadedPhotos: (files: UploadedPhotosState) => void
    setPreviewPhotos: (value: PreviewPhotosState) => void
    setIsLoading: (num: boolean) => void

}

export default function CreateSpotFormStepOne({setStep, setUploadedPhotos, setPreviewPhotos,setIsLoading}: Step1):JSX.Element{

    // TODO: add drag and drop for photo reordering
    return(
        <label 
            htmlFor="photos"
            className="group relative bg-neutral-100/60 hover:bg-neutral-200/40 hover:dark:bg-neutral-800/80 dark:bg-neutral-800/50 m-10 border-2 border-neutral-400/60 dark:border-white/30 border-dashed rounded-md w-auto h-full overflow-hidden transition-colors hover:cursor-pointer">
            <input 
                type="file" accept="image/png, image/jpeg, image/heic, image/heif"  
                name="photos" 
                id="photos"
                className="hidden" 
                onChange={(e) => {
                    setUploadedPhotos(e.target.files)
                    fileCompressionForPreview(e.target.files, setIsLoading, setPreviewPhotos)
                    setStep(2)
                }}
                multiple
                >
            </input>
            <div className="top-1/2 left-1/2 absolute flex flex-col justify-center items-center gap-4 -translate-1/2">
                <div className="flex justify-center items-center bg-neutral-50 dark:bg-neutral-700/40 p-4 border border-neutral-200 dark:border-none rounded-full w-20 h-20 group-hover:scale-110 transition-transform">
                    <Camera strokeWidth={1.5} className="stroke-neutral-500/80 dark:stroke-neutral-400/80 w-full h-full"/>
                </div>
                <div className="flex flex-col justify-center items-center gap-1">
                    <span className="font-semibold text-black dark:text-white/90 text-lg">Drag photos here</span>
                    <span className="text-neutral-500 text-sm">or click to browse</span>
                </div>
                
            </div>
        </label>
    )
}