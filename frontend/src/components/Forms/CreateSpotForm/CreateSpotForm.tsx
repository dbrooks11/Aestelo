import { useState, type JSX } from "react";
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
    const [previewPhotos, setPreviewPhotos] = useState<PreviewPhotosState>([])
    const [uploadedPhotos, setUploadedPhotos] = useState<UploadedPhotosState>(null)
    const [isLoading, setIsLoading] = useState<boolean>(false)
    const [step, setStep] = useState<StepState>(1)

    
// TODO: turn backend models and routes from 'post' to 'spot'
    function resetForm(): void {
        setPreviewPhotos([])
        setUploadedPhotos(null)
        setIsLoading(false)
        setStep(1)
    }

    return(
        <Modal 
            showModal={isCreateSpotModalOpen} 
            closeModal={() => {
                resetForm()
                setIsCreateSpotModalOpen(false)}}
            className="dark:bg-neutral-900 max-w-4xl"
            // TODO: remove close on bg click
            closeOnBgClick={true} 
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
                
                <div className="flex gap-4 items-center">
                    <button
                        className="px-4 py-1.5 rounded-full text-neutral-400 hover:dark:text-neutral-300 hover:text-neutral-500 text-center transition-colors cursor-pointer text-sm"
                        onClick={() => {
                            resetForm()
                            setIsCreateSpotModalOpen(false)}}
                    >
                        Cancel
                    </button>
                    {/* TODO: add save draft feature */}
                    {/* {step > 1 && <button>Save Draft</button>} */}
                    {(step !== 1 && step !== steps.length) && 
                    <button 
                        className="flex justify-center items-center gap-1 p-1 rounded-full text-neutral-700 dark:text-neutral-200 hover:dark:text-white hover:text-neutral-900 cursor-pointer"
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
                    className='flex flex-col flex-1 overflow-y-auto'
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
                        setStep={setStep}
                        setUploadedPhotos={setUploadedPhotos}
                        uploadedPhotos={uploadedPhotos}
                        previewPhotos={previewPhotos}
                        setPreviewPhotos={setPreviewPhotos}
                        setIsLoading={setIsLoading}
                        isLoading={isLoading}
                    />}

                    {/* Spot Details (Step 3) */}
                    {step === 3 && 
                    <CreateSpotFormStepThree
                        previewPhotos={previewPhotos}
                    />}
                
                </section>
            </div>
        </Modal>
    )
}