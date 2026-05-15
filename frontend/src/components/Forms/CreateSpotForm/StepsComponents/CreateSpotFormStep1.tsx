import { AlertTriangle, Camera } from "lucide-react";
import { type JSX } from "react";
import { type StepState, type UploadedPhotosState, type PreviewPhotosState } from "../CreateSpotForm";
import { fileCompressionForPreview } from "../../../../util/clientImageCompression";

export type Step1 = {
    setStep: (num: StepState) => void
    setUploadedPhotos: (files: UploadedPhotosState) => void
    setPreviewPhotos: (value: PreviewPhotosState) => void
    setIsLoading: (num: boolean) => void

}

export default function CreateSpotFormStepOne({setStep, setUploadedPhotos, setPreviewPhotos,setIsLoading}: Step1):JSX.Element{

    // TODO: add drag and drop for photo reordering
    return(
        <>
            <div className="bg-red-500/10 border border-red-500/20 rounded-lg px-4 py-3 flex gap-4 items-center shadow-sm shrink-0 mx-8 mt-4">
                <AlertTriangle className="text-red-400 shrink-0 mt-0.5" size={20} />
                <div className="flex-col flex gap-1">
                        <span className="text-xs font-bold text-red-400 uppercase tracking-wide">
                        Location Requirement
                        </span>
                        <p className="text-[11px] dark:text-neutral-400 text-neutral-600 leading-relaxed">
                        Your uploads rely on metadata to pinpoint the location of your spots and/or visits. 
                        <strong> Uploads will fail</strong> if photos lack GPS data or if the location varies significantly between photos.
                        </p>
                </div>
            </div>
            <label 
                htmlFor="photos"
                className="group relative bg-neutral-100/60 hover:bg-neutral-200/40 hover:dark:bg-neutral-800/80 dark:bg-neutral-800/50 mx-10 my-6 border-2 border-neutral-400/60 dark:border-white/30 border-dashed rounded-md w-auto h-full overflow-hidden transition-colors hover:cursor-pointer">
                <input 
                    type="file"  
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
        </>
    )
}