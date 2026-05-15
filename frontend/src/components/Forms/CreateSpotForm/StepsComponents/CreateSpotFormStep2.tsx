import { useEffect, useRef, useState, type Dispatch, type JSX, type SetStateAction } from "react";
import { type UploadedPhotosState, type PreviewPhotosState} from "../CreateSpotForm";
import { Scan, LoaderCircle, Trash2, Plus } from "lucide-react";
import { fileCompressionForPreview } from "../../../../util/clientImageCompression";
import ScrollContainer from "react-indiana-drag-scroll";


type Step2Type = {
    setUploadedPhotos: Dispatch<SetStateAction<UploadedPhotosState>>
    uploadedPhotos: UploadedPhotosState
    previewPhotos:PreviewPhotosState
    setPreviewPhotos: (value: PreviewPhotosState) => void
    isLoading: boolean
}

export default function CreateSpotFormStepTwo({setUploadedPhotos, uploadedPhotos, 
    previewPhotos, setPreviewPhotos, isLoading}: Step2Type):JSX.Element{
    
    const [isLoadingAddedPhotos, setIsLoadingAddedPhotos] = useState<boolean>(false)
    const [deletedPhotos, setDeletedPhotos] = useState<Array<number>>([])
    const [isDeleting, setIsDeleting] = useState<boolean>(false)
    const [currentPhoto, setCurrentPhoto] = useState<number>(0)
    const [aspectRatio, setAspectRatio] = useState<'Original' | '1/1' | '4/5'>('Original')

    const scrollRef = useRef<HTMLElement>(null)
    
    useEffect(() => {
        const element: HTMLElement | null = scrollRef.current
        if (!element) return

        const handleWheel = (e: WheelEvent): void => {
            if (e.deltaY !== 0) {
            e.preventDefault()
            
            element.scrollLeft += e.deltaY
            }
        };
        element.addEventListener('wheel', handleWheel, { passive: false })
        return () => element.removeEventListener('wheel', handleWheel)
    }, [])

    const showPreviews = () => {
        if(previewPhotos){
            const photoPreviewEl = previewPhotos.map((photo, index) => {
                return(
                    <div 
                        className={`${currentPhoto === index && 'scale-110 border-2 dark:border-accents-deep border-accents-primary'} 
                        ${isDeleting && deletedPhotos.includes(index) && 'opacity-30'} relative rounded-sm h-full aspect-4/5 overflow-hidden cursor-pointer transition-all`} 
                        onClick={() => {
                            if(isDeleting) togglePhotoDeletion(index)
                            else setCurrentPhoto(index)
                        }}
                        key={index}
                    >
                        <img 
                            loading="lazy"
                            decoding="async"
                            src={photo} 
                            className="w-full h-full object-cover"
                            draggable={false}
                            >
                        </img>
                        <div 
                            className='top-1 left-1 absolute flex justify-center items-center bg-black/60 rounded-full w-6 h-6 text-white select-none pointer-events-none'
                        >
                            {index + 1}
                        </div>
                    </div>
                )
            })
            return photoPreviewEl
        }
    }

    const handleAspectRatio = () => {
        if(aspectRatio === 'Original') {
            setAspectRatio('1/1')
        }else if(aspectRatio === '1/1'){
            setAspectRatio('4/5')
        } 
        else {
            setAspectRatio('Original')
        }
    }

    const showAspectAlias = () => {
        if(aspectRatio === '1/1') {
            return 'Square'
        }else if(aspectRatio === '4/5'){
            return 'Portrait'
        } 
        else {
            return 'Original'
        }
    }

    const togglePhotoDeletion = (index: number) => {
        if(deletedPhotos.includes(index)){
            setDeletedPhotos(prev => prev.filter(id => id !== index))
        }
        else{
            setDeletedPhotos(prev => [...prev, index])
        }
    }

    const handlePhotoDeletion = () => {
        if(deletedPhotos.length === 0){
            setIsDeleting(false)
            return
        }
        const currentFiles = Array.from(uploadedPhotos || [])
        const filesToKeep = currentFiles.filter((_, index) => !deletedPhotos.includes(index))

        const previewsToKeep = previewPhotos.filter((url, index) => {
            if(deletedPhotos.includes(index)){
                if(url){
                    URL.revokeObjectURL(url)
                    return false
                }
            }
            return true
        })

        setUploadedPhotos(arrayToFileList(filesToKeep))
        setPreviewPhotos(previewsToKeep)
        setDeletedPhotos([])
        setIsDeleting(false)
        setCurrentPhoto(0)
    }

    const arrayToFileList = (files: Array<File>) => {
        const newArray = new DataTransfer()
        files.forEach(file => newArray.items.add(file))
        return newArray.files
    }


    return(
        <div className="flex flex-col m-4 border border-neutral-200 dark:border-white/10 rounded-sm w-auto">
            <div className="relative flex justify-center items-center bg-neutral-100 dark:bg-black p-4 h-86">
                {!isLoading ?
                 <>
                    <img 
                        style={{ aspectRatio: aspectRatio !== 'Original' ? aspectRatio : undefined}}
                        className= "shadow-xl max-h-full object-cover"
                        src={previewPhotos && previewPhotos[currentPhoto]}
                    ></img>
                    <button 
                        type="button"
                        onClick={handleAspectRatio}
                        className="top-2 left-2 absolute flex justify-center items-center gap-2 px-2 py-1 border border-neutral-200 dark:border-white/15 rounded-full h-8 font-medium text-black dark:text-white text-xs cursor-pointer"
                    >
                        <Scan size={15}/>
                        {showAspectAlias()}
                    </button>
                    {isDeleting ? (
                            <div className="bottom-2 slide-in-from-bottom-2 absolute flex gap-2 animate-in fade-in">
                                <button
                                    type="button"
                                    onClick={() => {
                                        setIsDeleting(false);
                                        setDeletedPhotos([]);
                                    }}
                                    className="bg-neutral-100 hover:bg-white hover:dark:bg-neutral-600 dark:bg-neutral-800 px-4 py-2 border border-neutral-200 dark:border-none rounded-full w-26 font-bold text-black dark:text-white text-xs transition-colors cursor-pointer"
                                >
                                    Cancel
                                </button>
                                <button
                                    type="button"
                                    onClick={handlePhotoDeletion}
                                    className="flex items-center gap-2 bg-red-700 hover:bg-red-600 px-4 py-2 rounded-full font-bold text-white text-xs transition-colors cursor-pointer"
                                >
                                    <Trash2 size={14}/> Delete ({deletedPhotos.length})
                                </button>
                            </div>
                        ) : (
                            <button
                                type="button"
                                onClick={() => setIsDeleting(true)}
                                className="right-2 bottom-2 absolute bg-white hover:bg-red-500/50 hover:dark:bg-red-900/50 dark:bg-neutral-800/80 p-3 border border-neutral-300 hover:border-red-600/50 hover:dark:border-red-500/50 dark:border-white/10 rounded-full text-black dark:text-white transition-all cursor-pointe cursor-pointer"
                                title="Delete photos"
                            >
                                <Trash2 size={18}/>
                            </button>
                        )}
                </>: <LoaderCircle className="stroke-neutral-400 dark:stroke-white mx-auto animate-spin"/>}
                
            </div>
            <ScrollContainer innerRef={scrollRef} className="flex items-center border-neutral-200 dark:border-white/10 border-t min-h-40 shrink-0">
                {!isLoading ? <div className="flex justify-center items-center gap-4 mx-4 h-34">
                    {showPreviews()}
                    <label 
                        htmlFor="new_photos"
                        className="flex justify-center items-center border border-neutral-200 dark:border-white/10 rounded-sm h-full aspect-4/5 overflow-hidden text-neutral-500 hover:text-neutral-600 dark:hover:text-white dark:text-white/70 cursor-pointer"
                    >
                        {!isLoadingAddedPhotos ? <Plus/> : <LoaderCircle className="stroke-neutral-400 dark:stroke-white mx-auto transition-colors animate-spin"/>}
                    </label>
                    <input 
                        type="file" 
                        accept="image/png, image/jpeg, image/heic, image/heif"
                        name="new_photos"
                        id="new_photos"
                        className="hidden"
                        multiple
                        onChange={(e) => {
                            const newFiles = e.target.files
                            if(newFiles && newFiles.length > 0){
                                setUploadedPhotos((prev) => {
                                    const currentFiles = prev ? Array.from(prev) : []
                                    const addedFiles = Array.from(newFiles)
                                    const newFileArray = [...currentFiles, ...addedFiles]
                                    return arrayToFileList(newFileArray)
                                })
                            fileCompressionForPreview(e.target.files, setIsLoadingAddedPhotos, setPreviewPhotos)
                            }
                        }}
                    >
                    </input>
                </div>: <LoaderCircle className="stroke-neutral-400 dark:stroke-white mx-auto animate-spin"/>}
            </ScrollContainer>
        </div>
    )
}