import { useState, type JSX } from "react";
import Modal from "../../Modal";
import { type CreatePostFormModalOpenType } from "../../Wrappers/ProtectedRoute";
import { ArrowRight, Sun, Moon } from "lucide-react";
import CreatePostFormStepOne from "./StepsComponents/CreatePostFormStep1";
import CreatePostFormStepTwo from "./StepsComponents/CreatePostFormStep2";
import { useTheme } from "../../../context/ThemeContext";


export type PreviewPhotosState = Array<string | undefined> 
export type UploadedPhotosState = FileList | null
export type StepState = 1 | 2 | 3
type CreatePostForm = {
    isCreatePostModalOpen: CreatePostFormModalOpenType
    setIsCreatePostModalOpen: (value: CreatePostFormModalOpenType) => void
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
    }
]



// TODO: create save draft feature and add a table for drafts
export default function CreatePostForm({isCreatePostModalOpen, setIsCreatePostModalOpen}: CreatePostForm): JSX.Element{

    const {theme, toggleTheme} = useTheme()
    const [previewPhotos, setPreviewPhotos] = useState<PreviewPhotosState>([])
    const [uploadedPhotos, setUploadedPhotos] = useState<UploadedPhotosState>(null)
    const [isLoading, setIsLoading] = useState<boolean>(false)
    const [step, setStep] = useState<StepState>(1)

    const handlePostFormClick = async() => {

    }

    function resetForm(): void {
        setPreviewPhotos([])
        setUploadedPhotos(null)
        setStep(1)
    }

    return(
        <Modal 
            showModal={isCreatePostModalOpen} 
            closeModal={() => {
                resetForm()
                setIsCreatePostModalOpen(false)}}
            className="dark:bg-neutral-900"
            // TODO: remove close on bg click
            closeOnBgClick={true} 
        >
            
            <div className="relative flex justify-between items-center px-4 border-neutral-200 dark:border-neutral-800 border-b w-full h-16">
                <div className="flex items-center gap-4">
                    <span className="font-bold dark:text-white text-2xl">{steps[step -1].title}</span>
                    <button
                        className="flex justify-center items-center bg-black/5 hover:bg-black/10 hover:dark:bg-white/10 dark:bg-white/5 p-1.5 rounded-full w-8 h-8 dark:text-white/50 transition-colors cursor-pointer"
                        onClick={toggleTheme}
                    >
                        {theme === 'light' ? <Sun/> : <Moon/>}
                    </button>
                </div>
                
                <div>
                    {/* TODO: add save draft feature */}
                    {/* {step > 1 && <button>Save Draft</button>} */}
                    {step === 2 && <button className="flex justify-center items-center gap-1 p-1 rounded-full dark:text-neutral-500">Next<ArrowRight/></button>}
                </div>
            </div>
            <section
                className="flex flex-col flex-1 overflow-y-hidden"
            >
                <form
                    aria-label="Create Post form"
                    className={`flex flex-col flex-1 ${step === 2 && 'overflow-y-scroll'}`}
                >
                    {/* Upload Photos Box Input (Step 1) */}
                    {step === 1 && 
                    <CreatePostFormStepOne 
                        setStep={setStep}
                        setUploadedPhotos={setUploadedPhotos}
                        uploadedPhotos={uploadedPhotos}
                        setPreviewPhotos={setPreviewPhotos}
                        setIsLoading={setIsLoading}
                    />}

                    {/* Edit Photos (Step 2) */}
                    {step === 2 && 
                    <CreatePostFormStepTwo
                        setStep={setStep}
                        setUploadedPhotos={setUploadedPhotos}
                        uploadedPhotos={uploadedPhotos}
                        previewPhotos={previewPhotos}
                        setPreviewPhotos={setPreviewPhotos}
                        setIsLoading={setIsLoading}
                        isLoading={isLoading}
                    />}
                
                </form>
            </section>
        </Modal>
    )
}