import { useState, type FormEvent, type JSX, type KeyboardEvent } from "react";
import { ArrowLeft, ArrowRight, X, Accessibility } from "lucide-react";
import type { PreviewPhotosState, UploadedPhotosState } from "../CreateSpotForm";
import {protectedInstance } from "../../../../util/axiosHelpers";
import axios, { type AxiosResponse } from "axios";
import { useTaskStore } from "../../../../store/taskStateStore";
import toast from "react-hot-toast";

type Step3Type = {
    previewPhotos: PreviewPhotosState
    uploadedPhotos: UploadedPhotosState
    resetForm: () => void
    setIsLoading: (value:boolean) => void
}

export default function CreateSpotFormStepThree({previewPhotos, uploadedPhotos, resetForm, setIsLoading}: Step3Type): JSX.Element{

    const addTask = useTaskStore((state) => state.addTask)
    const [currentPhoto, setCurrentPhoto] = useState<number>(0)
    const [tags, setTags] = useState<Array<string | undefined>>([])
    const [tagInput, setTagInput] = useState<string>('')
    const [spotNameInput, setSpotNameInput] = useState<number>(0)
    const [descriptionInput, setDescriptionInput] = useState<number>(0)

    const spotNameMaxChars = 40
    const descriptionMaxChars = 200
    const tagsMaxChars = 50

    const handleSpotFormClick = async(e: FormEvent<HTMLFormElement>): Promise<void> => {
        e.preventDefault()
        let fileInfo: Array<{fileName: string, fileType: string}> = []
        setIsLoading(true)
        
        if(uploadedPhotos && uploadedPhotos.length > 0){
            const arrayUploadedPhotos: Array<File> = Array.from(uploadedPhotos)
            fileInfo = arrayUploadedPhotos.map((file) => ({
                fileName: file.name,
                fileType: file.type
            }))

            const formData = new FormData(e.currentTarget)

            // TODO: remove console logs and display actual errors via toast
            try{
                const responseOne: AxiosResponse = await protectedInstance.post('/s3/presigned-url/spot', fileInfo)

                if(responseOne.status === 200){
                    const presignedList: Array<{key: string, presigned_url: string}> = responseOne.data.message

                    try{
                        const uploadedPromises: Array<Promise<void | string>> = presignedList.map((presignedData, index: number) => {
                            const file = uploadedPhotos[index]

                            return axios.put(presignedData.presigned_url, file, {
                                headers: {
                                    "Content-Type": file.type
                                }
                            }).then(() => {
                                return presignedData.key
                            })
                        })

                        const uploadKeys: Array<void | string> = await Promise.all(uploadedPromises)
                        const formDataObj = Object.fromEntries(formData)

                        const responseTwo: AxiosResponse = await protectedInstance.post('/spot/create', {
                            name: formDataObj.name,
                            description: formDataObj.description,
                            accessibility: formDataObj.accessible ? true : false,
                            hashtags: tags,
                            keys: uploadKeys
                        })

                        if(responseTwo.status === 201){
                            const dataTwo = responseTwo.data
                            const {task_token, name, post_type } = dataTwo;

                            addTask(task_token, post_type, name);
                            resetForm()
                        }
                    }catch(error){
                        console.error(error)
                    }
                }
            }catch(error){
                console.error(error)
            }finally{
                setIsLoading(false)
            }
        }
    }

    const handleTags = (e: KeyboardEvent<HTMLInputElement>) => {
        if((e.key === 'Enter' || e.key === ' ') && tagInput?.trim()){
            if(tagInput.length > tagsMaxChars || tagInput.includes('#') || tagInput.includes(' ')) return
            if(!tags.includes(tagInput.trim())){
                setTags((prevTags) => {
                    return [...prevTags, tagInput.trim()]
                })
            }
            setTagInput('')
        }
    }

    const handleTagRemoval = (tag: string | undefined) => {
        if(tag){
            const newTagSet = tags.filter((tags) => tags !== tag)
            setTags(newTagSet)
        }
    }

    return (
        <div className="flex flex-1 h-full min-h-0 overflow-hidden">
    
            {/* LEFT SIDE: Image Preview Region */}
            <div 
                className="group relative bg-black w-1/2"
                role="region" 
                aria-label="Photo Preview Carousel"
            >
                <img 
                    src={previewPhotos[currentPhoto]} 
                    className="w-full h-full object-cover select-none"
                    alt={`Preview of photo ${currentPhoto + 1} of ${previewPhotos.length}`}
                />
                
                {/* Navigation Buttons */}
                <button 
                    className="hidden bottom-1/2 left-2 absolute group-hover:flex group-hover:bg-neutral-500/40 disabled:opacity-50 p-1 rounded-full text-white/80 hover:text-white transition-colors cursor-pointer"
                    type="button"
                    onClick={() => setCurrentPhoto(Math.max(0, currentPhoto - 1))}
                    disabled={currentPhoto === 0}
                    aria-label="Previous photo"
                >
                    <ArrowLeft size={26} aria-hidden="true"/>
                </button>
                
                <button 
                    className="hidden right-2 bottom-1/2 absolute group-hover:flex group-hover:bg-neutral-500/40 disabled:opacity-50 p-1 rounded-full text-white/80 hover:text-white transition-colors cursor-pointer"
                    type="button"
                    onClick={() => setCurrentPhoto(Math.min(previewPhotos.length - 1, currentPhoto + 1))}
                    disabled={currentPhoto === previewPhotos.length - 1}
                    aria-label="Next photo"
                >
                    <ArrowRight size={26} aria-hidden="true"/>
                </button>

                {/* Status Indicator */}
                <span 
                    className="top-4 right-2 absolute bg-neutral-500/40 px-2 py-0.5 border border-neutral-500/50 rounded-full text-white/90 text-xs tracking-widest"
                    role="status"
                    aria-live="polite"
                >
                    <span className="sr-only">Showing photo </span>
                    {currentPhoto + 1}
                    <span className="sr-only"> of </span>
                    /
                    {previewPhotos.length}
                </span>
            </div>

            {/* RIGHT SIDE: Form Region */}
            <form 
                id="create-spot-form"
                onSubmit={handleSpotFormClick}
                className="flex flex-col bg-white dark:bg-graphite border-neutral-200 dark:border-white/10 border-l w-1/2 h-full overflow-y-auto overscroll-y-contain transition-colors"
                aria-label="Spot Details Form"
            >
                <div className="flex flex-col gap-8 p-4">

                    {/* Spot Name */}
                    <div className="flex flex-col gap-2 font-semibold text-neutral-600 dark:text-neutral-500">
                        <label htmlFor="name" className="text-xs uppercase tracking-wider">Spot Name</label>
                        <input 
                            type="text" 
                            id="name" 
                            name="name"
                            maxLength={40}
                            onChange={(e) => {
                                const value = e.target.value

                                if(value.length > spotNameMaxChars){
                                    e.target.value = value.slice(0, spotNameMaxChars)
                                }
                                setSpotNameInput((e.target.value).length)
                            }}
                            aria-describedby="name-char-count"
                            className="bg-transparent px-4 py-2 border border-neutral-200 focus:border-neutral-400 focus:dark:border-white/20 dark:border-white/10 rounded-md outline-none text-neutral-900 dark:placeholder:text-white/20 dark:text-white placeholder:text-neutral-400 placeholder:text-sm transition-colors"
                            placeholder="e.g. Hidden Skate Park"
                        />
                        <span 
                            id="name-char-count" 
                            className="ml-1 text-[10px] text-neutral-400 dark:text-neutral-500"
                            aria-live="polite"
                        >
                            Max characters {spotNameInput}/40
                        </span>
                    </div>

                    {/* Description */}
                    <div className="flex flex-col gap-2 font-semibold text-neutral-600 dark:text-neutral-500">
                        <label htmlFor="description" className="text-xs uppercase tracking-wider">Description</label>
                        <textarea 
                            id="description" 
                            name="description" 
                            onChange={(e) => {
                                const value = e.target.value

                                if(value.length > descriptionMaxChars){
                                    e.target.value = value.slice(0, descriptionMaxChars)
                                }

                                setDescriptionInput((e.target.value).length)
                            }}
                            aria-describedby="desc-char-count"
                            className="bg-transparent px-4 py-2 border border-neutral-200 focus:border-neutral-400 focus:dark:border-white/20 dark:border-white/10 rounded-md outline-none min-h-[120px] text-neutral-900 dark:placeholder:text-white/20 dark:text-white placeholder:text-neutral-400 placeholder:text-sm transition-colors resize-none" 
                            maxLength={200}
                            placeholder="Tell us about this spot..."
                        />
                        <span 
                            id="desc-char-count" 
                            className="ml-1 text-[10px] text-neutral-400 dark:text-neutral-500"
                            aria-live="polite"
                        >
                            Max characters {descriptionInput}/200
                        </span>
                    </div>

                    {/* Accessible checkbox */}
                    <div className="flex">
                        <label
                            htmlFor="accessible"
                            className="flex justify-center items-center gap-4 text-neutral-600 dark:text-neutral-500 text-sm cursor-pointer"
                        >
                            <input
                                type="checkbox"
                                name="accessible"
                                id="accessible"
                                className="sr-only peer"
                            />
                            <div className="flex justify-center items-center bg-transparent border-2 border-neutral-200 dark:border-neutral-600 dark:group-hover:border-neutral-400 group-hover:border-neutral-500 peer-checked:border-blue-800 rounded-md w-6 h-6 text-transparent peer-checked:dark:text-white/90 peer-checked:text-black transition-all duration-200"
                            >
                                <Accessibility strokeWidth={3} className="w-3.5 h-3.5" />
                            </div>
                            Wheelchair Accessible
                        </label>
                    </div>

                    {/* Hashtags */}
                    <div className="flex flex-col gap-2 font-semibold text-neutral-600 dark:text-neutral-500">
                        <label htmlFor="tags" className="text-xs uppercase tracking-wider">Hashtags</label>
                        <div 
                            className="flex flex-wrap gap-2 px-4 py-2 border border-neutral-200 focus-within:border-neutral-400 focus-within:dark:border-white/20 dark:border-white/10 rounded-md w-full text-neutral-900 dark:text-white transition-colors" 
                        >
                            {tags.map((tag) => (
                                <span
                                    key={tag}
                                    className="flex items-center gap-1 bg-neutral-100 dark:bg-white/10 shadow-sm px-2 py-1 border border-neutral-200 dark:border-white/5 rounded max-w-full h-min text-neutral-700 dark:text-neutral-200 text-xs break-all lg:break-normal"
                                >
                                    #{tag}
                                    <button 
                                        type='button' 
                                        className="flex justify-center items-center hover:text-black dark:hover:text-white transition-colors cursor-pointer"
                                        onClick={() => handleTagRemoval(tag)}
                                        aria-label={`Remove tag ${tag}`}
                                    >
                                        <X size={14}/>
                                    </button>
                                </span>
                            ))}
                            <input
                                type="text"
                                id="tags" 
                                name="tags" 
                                className="flex-1 bg-transparent outline-none min-w-[120px] dark:placeholder:text-white/20 placeholder:text-neutral-400 placeholder:text-sm"
                                value={tagInput}
                                onChange={(e) => setTagInput(e.target.value)}
                                onKeyDown={(e) => {
                                    if(e.key === 'Enter' || e.key === ' '){
                                        e.preventDefault()
                                        handleTags(e)
                                    }
                                    
                                }}
                                placeholder="Add hashtag..."
                                aria-describedby="tags-hint"
                            />
                        </div>
                        <span 
                            id="tags-hint" 
                            className="ml-1 text-[10px] text-neutral-400 dark:text-neutral-500"
                        >
                            Press Space or Enter to add tags. Max characters per tag {tagInput.length}/50
                        </span>
                    </div>
                    
                </div>
            </form>
        </div>
    )
}
