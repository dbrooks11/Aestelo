import { type JSX, useEffect, type ReactNode, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import ToasterCustom from "./Toast";
import cn from "../util/tailwind_merger";

type ModalProps = {
    showModal: boolean
    closeModal: () => void
    closeOnBgClick?: boolean
    children: ReactNode
    className?: string
    dialogClassName?: string
    preventDefault?: boolean
    preventPropagation?: boolean
}


export default function Modal({showModal, closeModal, closeOnBgClick ,
  children, className, dialogClassName, preventDefault, preventPropagation}: ModalProps): JSX.Element {    
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
      onClick={
        (e) => {
          if(preventPropagation) e.stopPropagation()
          if(preventDefault) e.preventDefault()
          if(closeOnBgClick && e.target === dialogRef.current) closeModal()
        }
        
      }
      className={`${cn('bg-transparent backdrop:bg-black/30 backdrop-blur-xs min-w-full min-h-full md:overflow-y-auto', dialogClassName)}`}
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >   
      <AnimatePresence initial={false}>
        {showModal ? (
          <motion.div
            key="modal"
            initial={{ opacity: 0, scale: 0 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0 }}
            className={cn(`flex flex-col bg-bg-modal-light dark:bg-bg-modal-dark mx-auto my-20 border border-border-color-light dark:border-border-color-dark rounded-xl max-w-3xl h-140 overflow-hidden`, className)}
          >
              {children}
          </motion.div>
        ) : null}
      </AnimatePresence>
      <ToasterCustom toasterId="modal"/>
    </dialog>
  )
}