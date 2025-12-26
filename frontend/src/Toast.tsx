import toast from "react-hot-toast"

export const toastNotifyMessage = (message:string) => {
      toast(message)
}

export const toastNotifySuccess = (message:string) => {
      toast.success(message)
}

export const toastNotifyError = (message:string) => {
      toast.error(message)
}

export const toastNotifyLoading = (message:string) => {
      toast.loading(message)
}

export const toastNotifyCustom = (message:string) => {
      toast.custom(message)
}