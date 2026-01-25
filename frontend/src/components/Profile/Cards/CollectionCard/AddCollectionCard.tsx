import { BookmarkPlusIcon } from "lucide-react";
import { type JSX } from "react";
import Modal from "../../../Modal";

export default function AddCollectionCard(): JSX.Element{

    

    return(
        <>
            <button 
                type="button"
                className="flex flex-col justify-center items-center gap-1 border border-black/10 hover:border-black/20 hover:dark:border-white/15 dark:border-white/5 rounded-sm aspect-square overflow-hidden font-semibold text-neutral-600 hover:dark:text-neutral-400 hover:text-neutral-700 dark:text-neutral-500 text-xs md:text-base transition-colors cursor-pointer shrink-0"
            >
                <BookmarkPlusIcon/>
                <span className="">New Collection</span>
            </button>
        </>
    )
}