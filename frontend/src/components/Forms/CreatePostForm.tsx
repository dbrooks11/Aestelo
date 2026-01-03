import { useState, type Dispatch, type JSX, type SetStateAction } from "react";
import Modal from "../Modal";
import { ArrowRight, Camera } from "lucide-react";

type CreatePostFormProps = {
    isCreatePostModalOpen: boolean
    setIsCreatePostModalOpen: Dispatch<SetStateAction<boolean>>
}

// TODO: create save draft feature and add table for drafts
export default function CreatePostForm({isCreatePostModalOpen, setIsCreatePostModalOpen}: CreatePostFormProps): JSX.Element{

    const [uploadedPhotos, setUploadedPhotos] = useState<FileList | null>(null)
    const [step, setStep] = useState< 1 | 2 | 3>(1)

    const handlePostFormClick = async() => {

    }

    console.log(uploadedPhotos)

    return(
        <Modal 
            showModal={isCreatePostModalOpen} 
            closeModal={() => setIsCreatePostModalOpen(false)}
            className="dark:bg-neutral-900"
            // TODO: remove close on bg click
            closeOnBgClick={true} 
        >
            <div className="flex items-center justify-between w-full h-16 px-4">
                <span className="dark:text-white font-bold text-2xl">Select Photos</span>
                <div>
                    {/* TODO: add save draft feature */}
                    {/* <button>Save Draft</button> */}
                    {step === 2 && <button className="flex items-center justify-center p-1 rounded-full dark:text-neutral-500 gap-1">Next<ArrowRight/></button>}
                </div>
            </div>
            <section
                className="flex flex-col flex-1 w-full overflow-y-hidden"
            >
                <form
                    aria-label="Create Post form"
                    action={handlePostFormClick}
                    className="flex flex-col flex-1 m-10"
                >
                    <label 
                        htmlFor="photos"
                        className="w-full h-full border-2 border-dashed border-white/30 rounded-md overflow-hidden relative 
                    bg-neutral-800/50 hover:bg-neutral-800/80 group transition-colors hover:cursor-pointer">
                        
                        <input 
                            type="file" accept="image/png, image/jpeg, image/heic, image/heif"  
                            name="photos" 
                            id="photos"
                            className="hidden" 
                            onChange={(e) => setUploadedPhotos(e.target.files)}
                            multiple
                            >
                        </input>
                        <div className="flex flex-col gap-4 absolute top-1/2 left-1/2 -translate-1/2 items-center justify-center">
                            <div className="rounded-full h-20 w-20 flex items-center justify-center group-hover:scale-110 
                            transition-transform bg-neutral-700/40 p-4">
                                <Camera strokeWidth={1.5} className="stroke-neutral-400/80 w-full h-full"/>
                            </div>
                            <div className="flex flex-col items-center justify-center gap-1">
                                <span className="text-white/90 font-semibold text-lg">Drag photos here</span>
                                <span className="text-neutral-500 text-sm">or click to browse</span>
                            </div>
                            
                        </div>
                    </label>
                </form>
            </section>
        </Modal>
    )
}