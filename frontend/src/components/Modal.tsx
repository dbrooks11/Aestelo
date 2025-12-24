import { type JSX, useEffect, type ReactNode, useRef } from "react";
import { X } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

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
        onCancel={closeModal}
        onClick={closeOnBgClick ? (e) => e.target === dialogRef.current && closeModal(): undefined}
        className="backdrop:bg-black/30 bg-transparent min-w-full min-h-full"
        >   
            <AnimatePresence initial={false}>
                {showModal ? <motion.div
                key="modal"
                initial={{ opacity: 0, scale: 0 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0 }}
                className="max-w-2/4 h-120 mx-auto mt-30 dark:bg-charcoal border dark:border-neutral-500 rounded-lg flex flex-col">

                    {/* Title and Exit Button */}
                    <div className="flex p-2 justify-between">
                        <h2 className="text-2xl dark:text-white font-bold items-center justify-center">{title}</h2>
                        <button onClick={closeModal} className="w-8 h-8 rounded-full hover:cursor-pointer text-black dark:text-white dark:hover:bg-accents-deep/50"><X className="w-full h-full"/></button>
                    </div>

                    {/* Content */}
                    <section className="flex flex-col w-full flex-1 overflow-hidden">
                        {children}
                    </section>
                </motion.div>: null}
            </AnimatePresence>
        </dialog>
    )
}