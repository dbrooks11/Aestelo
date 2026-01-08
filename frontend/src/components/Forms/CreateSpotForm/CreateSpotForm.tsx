import { useEffect, useRef, useState, type JSX } from "react";
import Modal from "../../Modal";
import { type CreateSpotFormModalOpenType } from "../../Wrappers/ProtectedRoute";
import { ArrowRight, Sun, Moon, ChevronLeft } from "lucide-react";
import CreateSpotFormStepOne from "./StepsComponents/CreateSpotFormStep1";
import CreateSpotFormStepTwo from "./StepsComponents/CreateSpotFormStep2";
import { useTheme } from "../../../context/ThemeContext";
import CreateSpotFormStepThree from "./StepsComponents/CreateSpotFormStep3";


export type PreviewPhotosState = Array<string | undefined> 
export type UploadedPhotosState = FileList | null
export type StepState = 1 | 2 | 3
type CreateSpotForm = {
    isCreateSpotModalOpen: CreateSpotFormModalOpenType
    setIsCreateSpotModalOpen: (value: CreateSpotFormModalOpenType) => void
}
type Steps = {
    stepOrder: number
    title: string
}

const steps: Array<Steps> = [
    {
        stepOrder: 1,
        title: "Select Photos"
    },
    {
        stepOrder: 2,
        title: "Edit Photos"
    },
    {
        stepOrder: 3,
        title: 'Spot Details'
    }
]



// TODO: create save draft feature and add a table for drafts
export default function CreateSpotForm({isCreateSpotModalOpen, setIsCreateSpotModalOpen}: CreateSpotForm): JSX.Element{

    const {theme, toggleTheme} = useTheme()
    const dialogRef = useRef<HTMLDialogElement>(null)
    const [showConfirmation, setShowConfirmation] = useState<boolean>(false)
    const [previewPhotos, setPreviewPhotos] = useState<PreviewPhotosState>([])
    const [uploadedPhotos, setUploadedPhotos] = useState<UploadedPhotosState>(null)
    const [isLoading, setIsLoading] = useState<boolean>(false)
    const [step, setStep] = useState<StepState>(1)

    useEffect(() => {
        if(showConfirmation) dialogRef.current?.showModal()
        else if (!showConfirmation) dialogRef.current?.close()
        
    }, [showConfirmation]);
    
// TODO: turn backend models and routes from 'post' to 'spot'
    function resetForm(): void {
        setShowConfirmation(false)
        setPreviewPhotos([])
        setUploadedPhotos(null)
        setIsLoading(false)
        setStep(1)
        setIsCreateSpotModalOpen(false)
    }

    return(
        <Modal 
            showModal={isCreateSpotModalOpen} 
            closeModal={() => resetForm()}
            className="dark:bg-neutral-900 max-w-4xl"
            closeOnBgClick={false} 
        >
            
            {/* Form Title */}
            <div className="relative flex justify-between items-center px-4 border-neutral-200 dark:border-neutral-800 border-b w-full h-16">
                <div className="flex items-center gap-4">
                    {step > 2 && 
                    <ChevronLeft 
                        className="hover:stroke-neutral-200 dark:stroke-neutral-400 transition-colors cursor-pointer"
                        onClick={() => {
                            setStep((prev) => {
                                return prev - 1
                            })
                        }}
                    />
                    }
                    <span 
                        className="flex items-center gap-4 font-bold dark:text-white text-2xl"
                        >
                            {steps[step - 1].title}
                    </span>
                    <button
                        className="flex justify-center items-center bg-black/5 hover:bg-black/10 hover:dark:bg-white/10 dark:bg-white/5 p-1.5 rounded-full w-8 h-8 dark:text-white/50 transition-colors cursor-pointer"
                        onClick={toggleTheme}
                    >
                        {theme === 'light' ? <Sun/> : <Moon/>}
                    </button>
                </div>
                
                <div className="flex items-center gap-4">
                    <button
                        className="px-4 py-1.5 rounded-full text-neutral-400 hover:dark:text-neutral-300 hover:text-neutral-500 text-sm text-center transition-colors cursor-pointer"
                        onClick={() => setShowConfirmation(true)}
                    >
                        Cancel
                    </button>
                    {/* TODO: add save draft feature */}
                    {/* {step > 1 && <button>Save Draft</button>} */}
                    {(step !== 1 && step !== steps.length) && 
                    <button 
                        className="flex justify-center items-center gap-1 p-1 rounded-full text-neutral-700 hover:dark:text-white hover:text-neutral-900 dark:text-neutral-200 cursor-pointer"
                        onClick={() => {
                            setStep((prev) => {
                                return prev + 1
                            })
                        }}
                        >Next<ArrowRight size={22}/>
                    </button>
                    }
                    {step === steps.length && 
                        <button 
                            type="submit" 
                            form="create-spot-form" 
                            className="bg-black/90 hover:bg-black hover:dark:bg-white dark:bg-white/90 hover:shadow-md px-4 py-1.5 rounded-full text-white dark:text-black text-center transition-colors cursor-pointer"
                        >Create</button>
                    }
                </div>
            </div>
            <div
                className="flex flex-col flex-1 overflow-y-hidden"
            >
                <section
                    aria-label="Create Spot form"
                    className='relative flex flex-col flex-1 overflow-y-auto'
                >
                    {/* Upload Photos Box Input (Step 1) */}
                    {step === 1 && 
                    <CreateSpotFormStepOne 
                        setStep={setStep}
                        setUploadedPhotos={setUploadedPhotos}
                        setPreviewPhotos={setPreviewPhotos}
                        setIsLoading={setIsLoading}
                    />}

                    {/* Edit Photos (Step 2) */}
                    {step === 2 && 
                    <CreateSpotFormStepTwo
                        setUploadedPhotos={setUploadedPhotos}
                        uploadedPhotos={uploadedPhotos}
                        previewPhotos={previewPhotos}
                        setPreviewPhotos={setPreviewPhotos}
                        isLoading={isLoading}
                    />}

                    {/* Spot Details (Step 3) */}
                    {step === 3 && 
                    <CreateSpotFormStepThree
                        previewPhotos={previewPhotos}
                    />}

                    {showConfirmation && 
                    <dialog
                        ref={dialogRef}
                        className="bg-neutral-100 dark:bg-neutral-900 shadow-2xl m-auto p-6 border border-neutral-300 dark:border-white/10 rounded-xl w-full max-w-sm text-black dark:text-white"
                        onClose={() => setShowConfirmation(false)}
                        aria-labelledby="dialog-title"
                        aria-describedby="dialog-desc"
                    >
                        <div className="flex flex-col items-center gap-4 text-center">
                            <span 
                                id="dialog-title" 
                                className="font-bold text-lg"
                            >
                                Discard Spot?
                            </span>
                            
                            <span 
                                id="dialog-desc" 
                                className="text-neutral-500 dark:text-neutral-400 text-sm"
                            >
                                If you leave now, all your progress will be lost.
                            </span>
                            
                            <div className="flex gap-3 mt-2 w-full">
                                {/* Cancel / Keep Editing Button */}
                                <button 
                                    className="flex-1 bg-neutral-100 hover:bg-neutral-200 dark:bg-white/5 dark:hover:bg-white/10 px-4 py-2 border border-neutral-200 dark:border-white/10 rounded-lg font-medium text-neutral-700 dark:text-white transition-colors cursor-pointer"
                                    onClick={() => setShowConfirmation(false)}
                                    autoFocus
                                >
                                    No, Keep Editing
                                </button>
                                
                                {/* Confirm / Discard Button */}
                                <button 
                                    className="flex-1 bg-red-50 hover:bg-red-100 dark:bg-red-500/10 dark:hover:bg-red-500/20 px-4 py-2 border border-red-200 dark:border-red-500/20 rounded-lg font-medium text-red-600 dark:text-red-400 transition-colors cursor-pointer"
                                    onClick={() => {
                                        dialogRef.current?.close()
                                        resetForm()
                                    }}
                                >
                                    Yes, Discard
                                </button>
                            </div>
                        </div>
                    </dialog>
                    }
                
                </section>
            </div>
        </Modal>
    )
}