import { Toaster, type ToastPosition } from 'react-hot-toast';
import { type JSX } from 'react';


type ToasterCustomType = {
    position?: ToastPosition,
    removeDelay?: number,
    toasterId?: string
}

export default function ToasterCustom({position, removeDelay, toasterId}:ToasterCustomType): JSX.Element{
    return (
    <>  
        <Toaster
        position= {position ? position : "top-center"}

        toasterId={toasterId}

        toastOptions={{
            removeDelay: removeDelay ? removeDelay : 1000,
            className: 'bg-white dark:bg-charcoal text-black dark:text-white border border-gray-200 dark:border-white/10 shadow-lg',
            
            success: {
            className: 'bg-green-50 dark:bg-green-900/20 text-green-800 dark:text-green-200 border border-green-200 dark:border-green-800',
            iconTheme: {
                primary: '#10B981',
                secondary: 'white',
            },
            },
            error: {
            className: 'bg-red-50 dark:bg-red-900/20 text-red-800 dark:text-red-200 border border-red-200 dark:border-red-800',
            iconTheme: {
                primary: '#EF4444',
                secondary: 'white',
            },
            },
        }}
        />
    </>
    );
}
    