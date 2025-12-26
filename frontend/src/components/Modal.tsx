import { type JSX, useEffect, type ReactNode, useRef } from "react";
import { X } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { Toaster } from "react-hot-toast";
import ToasterCustom from "./Toast";

type ModalProps = {
    showModal: boolean
    closeModal: () => void
    title?: string
    closeOnBgClick?: boolean
    children: ReactNode
}


export default function Modal({showModal, closeModal, title, closeOnBgClick ,children}: ModalProps): JSX.Element {    
    const dialogRef = useRef<HTMLDialogElement>(null)
    
    useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;

    if (showModal) {
      dialog.showModal()
      document.body.style.overflow = "hidden"
    } else {
      dialog.close()
      document.body.style.overflow = "unset"
    }

    return () =>{
        document.body.style.overflow = "unset"
    }
  }, [showModal]);

    return(
        <dialog
        ref={dialogRef}
        onClick={closeOnBgClick ? (e) => e.target === dialogRef.current && closeModal(): undefined}
        className="bg-transparent backdrop:bg-black/30 min-w-full min-h-full px-4 backdrop-blur-xs"
        >   
            <AnimatePresence initial={false}>
                {showModal ? <motion.div
                key="modal"
                initial={{ opacity: 0, scale: 0 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0 }}
                className="flex flex-col dark:bg-bg-modal-dark bg-bg-modal-light mx-auto my-20 border dark:border-border-color-dark border-border-color-light rounded-2xl max-w-3xl h-140 overflow-hidden">

                    {/* Title and Exit Button */}
                    <div className="flex justify-between p-3 border-b border-border-color-light dark:border-border-color-dark dark:bg-bg-secondary-dark rounded-t-2xl">
                        <h2 className="justify-center items-center font-semibold dark:text-white text-2xl">{title}</h2>
                        <button onClick={closeModal} className="dark:hover:bg-accents-deep/40 rounded-full w-8 h-8 text-black dark:text-white transition-colors hover:cursor-pointer p-1"><X className="w-full h-full"/></button>
                    </div>

                    {/* Content */}
                    <section className="flex flex-col flex-1 w-full overflow-y-hidden">
                        {children}
                    </section>
                    <ToasterCustom toasterId="modal"/>
                </motion.div>: null}
            </AnimatePresence>
        </dialog>
    )
}