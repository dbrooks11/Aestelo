import { useState, useEffect,type Dispatch, type JSX, type SetStateAction, type ChangeEvent } from "react";
import cn from "../../util/tailwind_merger";
import { type ProfileDataType } from "../../pages/ProfilePage";
import { LoaderCircle, PencilLine, X } from 'lucide-react'
import toast from "react-hot-toast";
import { Monitor, Smartphone, Upload } from "lucide-react";
import { protectedInstance } from "../../util/axios_api_helpers";
import { useFormStatus } from "react-dom";
import { AxiosErrorHelper } from "../../util/axios_api_helpers";
import Modal from "../Modal";

type EditProfileFormProps = {
  profile_banner_url: ProfileDataType['profile_banner_url']
  profile_photo_url: ProfileDataType['profile_photo_url']
  username: ProfileDataType['username']
  bio: ProfileDataType['bio']
  setProfileData: Dispatch<SetStateAction<ProfileDataType | null>>
  setShowModal: (value: boolean) => void
  showModal: boolean
}

const editProfileFormScreenGuideButtonStyle = 'flex gap-2 py-1 px-2 items-center rounded-md hover:dark:text-text-main-dark hover:text-text-main-light cursor-pointer'
const editProfileFormScreenGuideButtonActiveStyle = 'dark:bg-bg-secondary-dark bg-bg-secondary-light dark:text-text-main-dark text-text-main-light shadow-sm'
const editProfileFormContainerStyle = 'border dark:bg-charcoal dark:border-border-color-dark bg-black/10 border-border-color-light rounded-lg text-sm'
const editProfileFormLabelStyle = 'font-bold dark:text-text-muted-dark text-text-main-light'
const editProfileFormTinyText = 'text-[10px] text-text-muted-light dark:text-text-muted-dark'

export default function EditProfileForm({
  username, bio, profile_photo_url, profile_banner_url,
  setProfileData, setShowModal, showModal }: EditProfileFormProps): JSX.Element {
  
  const [usernameIndicator, setUsernameIndictor] = useState<boolean>(false)
  const [charCounterBio, setCharCounterBio] = useState<number>(bio.length) 
  const [charCounterUsername, setCharCounterUsername] = useState<number>(username.length) 
  const [screenGuideType, setScreenGuideType] = useState<'mobile' | 'desktop'>('desktop')
  const [profilePhotoPreview, setProfilePhotoPreview] = useState<string | undefined>(undefined)
  const [profileBannerPreview, setProfileBannerPreview] = useState<string | undefined>(undefined)

  const handleProfilePhotoFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    let tempUrl: string = ''
    if (e.target.files) {
      tempUrl = URL.createObjectURL(e.target.files[0])
      setProfilePhotoPreview(tempUrl)
    }
  }

  const handleProfileBannerFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    let tempUrl: string = ''
    if (e.target.files) {
      tempUrl = URL.createObjectURL(e.target.files[0])
      setProfileBannerPreview(tempUrl)
    }

  }

  useEffect(() => {
    return () => {
      if (profilePhotoPreview) {
        URL.revokeObjectURL(profilePhotoPreview);
      }
      if (profileBannerPreview) {
        URL.revokeObjectURL(profileBannerPreview);
      }
    };
  },);

  //TODO: Add field for links and badges(maybe) in the future
  const handleEditProfileFormClick = async (formData: FormData): Promise<void> => {
    try {
      const response = await protectedInstance.patch('/profile/me', formData, {
        headers:{
          'Content-Type': 'multipart/form-data'
        }
      })

      if (response.status === 200) {
        const data = response.data

        setProfileData((prev) => {
          if (!prev) return null;
          return (
            {
              ...prev,
              profile_banner_url: data.updated_fields.profile_banner_url,
              profile_photo_url: data.updated_fields.profile_photo_url,
              username: data.updated_fields.username,
              bio: data.updated_fields.bio
            }
          )
        })
        setShowModal(false)
        toast.success(data.message, {
          toasterId: 'profile'
        })
      }
    } catch(error) {
      const newError = AxiosErrorHelper(error)
      toast.error(newError, {
        toasterId: 'modal'
      })
      setProfileBannerPreview(profile_banner_url)
      setProfilePhotoPreview(profile_photo_url)
    }
  }

  //TODO: export submit button from signup or login an customize css
  function SubmitButton():JSX.Element{
    const {pending} = useFormStatus()

    return(
      <>
        <button
          type='submit'
          className={`${!pending && `hover:bg-accents-primary hover:shadow-md`} flex justify-center items-center bg-accents-deep  p-3 rounded-md w-1/2 cursor-pointer`}
          disabled = {pending}
          >{pending ? <LoaderCircle className="mr-2 animate-spin"/>: null}{pending ? 'Confirming' : 'Confirm'}
        </button>
      </>
    )
  }

  const charCounterBioDisplayHandler = (e: ChangeEvent<HTMLTextAreaElement>) =>{
    const length = e.target.value.length
    setCharCounterBio(length)
  }
    

  const charCounterUsernameDisplayHander = (e: ChangeEvent<HTMLInputElement>) =>{
    const length = e.target.value.length
    setCharCounterUsername(length)
  }

  const usernameIndicatorHander = (e: ChangeEvent<HTMLInputElement>) => {
    const usernameChars = e.target.value
    const re = /^[0-9A-Za-z_.]+$/

    if(e.target.value === '' || !re.test(usernameChars)){
      setUsernameIndictor(true)
    }else{
      setUsernameIndictor(false)
    }

    charCounterUsernameDisplayHander(e)
  }



  return (   
    <Modal showModal={showModal} closeModal={() => setShowModal(false)}>
      
      {/* Form Header */}
      <div className="flex justify-between dark:bg-bg-secondary-dark p-3 border-border-color-light dark:border-border-color-dark border-b rounded-t-2xl">
        <h2 
          id="modal-title" 
          className="justify-center items-center font-semibold dark:text-white text-2xl"
        >
          Edit Profile
        </h2>
        
        <button 
          onClick={() => setShowModal(false)} 
          className="dark:hover:bg-accents-deep/40 p-1 rounded-full w-8 h-8 text-black dark:text-white transition-colors hover:cursor-pointer"
          aria-label="Close Modal"
        >
          <X className="w-full h-full" aria-hidden="true" />
        </button>
      </div>

      {/* Form Section */}
      <section className="flex flex-col flex-1 w-full overflow-y-hidden">
        <form 
          action={handleEditProfileFormClick} 
          className='flex flex-col flex-1 items-center gap-10 px-6 overflow-y-scroll text-white'
          aria-label="Edit Profile Form"
        >
              
          {/* Profile Picture */}
          <div className='flex items-center gap-[5%] md:gap-45 mt-6 w-full'>
            <label htmlFor='profile_photo' className={editProfileFormLabelStyle}>Profile Picture</label>
            
            <div className={cn(`${editProfileFormContainerStyle} relative`, 'rounded-full')}>
              <div className="w-35 h-35">
                <img
                  src={profilePhotoPreview ? profilePhotoPreview : profile_photo_url}
                  className='rounded-full w-full h-full object-cover pointer-events-none'
                  alt="Profile Picture Preview"
                ></img>
              </div>
              
              <label 
                htmlFor='profile_photo' 
                className='top-25 left-25 absolute bg-black/15 dark:bg-white/10 backdrop-blur-sm p-2 rounded-full w-9 cursor-pointer'
                aria-label="Change Profile Picture Button"
              >
                <PencilLine className='w-full h-full' strokeWidth={1} aria-hidden="true" />
              </label>
            </div>

            <input
              type='file'
              name='profile_photo'
              id='profile_photo'
              className='hidden'
              accept='image/png, image/jpeg, image/heic, image/heif'
              onChange={handleProfilePhotoFileChange}
              multiple={true} 
            ></input>
          </div>

          {/* Profile Banner */}
          <div className="flex flex-col gap-4 mt-4 w-full">
            
            <div className="flex justify-between items-center">
              <h2 className={editProfileFormLabelStyle}>Profile Banner</h2>
              
              <label 
                htmlFor="profile_banner" 
                className="flex items-center gap-2 text-accents-primary text-sm hover:underline cursor-pointer"
                role="button"
                tabIndex={0}
              >
                <Upload size={20} aria-hidden="true" /> Change Image
              </label>
            </div>

            <div 
              className={`${editProfileFormContainerStyle} w-50 flex justify-between border p-1 dark:text-text-muted-dark text-text-muted-light font-bold mx-auto md:mx-0`}
              role="group" 
              aria-label="Banner Preview Mode"
            >
              <button
                className={cn(editProfileFormScreenGuideButtonStyle, `${screenGuideType === 'desktop' && editProfileFormScreenGuideButtonActiveStyle}`)}
                type="button"
                onClick={() => setScreenGuideType('desktop')}
                aria-pressed={screenGuideType === 'desktop'}
              >
                <Monitor size={18} aria-hidden="true" /> Desktop
              </button>
              
              <button
                className={cn(editProfileFormScreenGuideButtonStyle, `${screenGuideType === 'mobile' && editProfileFormScreenGuideButtonActiveStyle}`)}
                type="button"
                onClick={() => setScreenGuideType('mobile')}
                aria-pressed={screenGuideType === 'mobile'}
              >
                <Smartphone size={18} aria-hidden="true" /> Mobile
              </button>
            </div>

            <div 
              className={`${editProfileFormContainerStyle} min-h-60 flex items-center justify-center w-full py-8`}
              aria-hidden="true" 
            >
              <div
                className={`${screenGuideType === 'desktop' ? 'w-full aspect-3/1' : 'w-100 aspect-15/16'} border-4 border-black bg-black rounded-lg overflow-hidden transition-all relative shadow-lg`}
              >
                <img 
                  src={profileBannerPreview ? profileBannerPreview : profile_banner_url}
                  className={`${screenGuideType === 'desktop' && 'object-[10%_52%]'} h-full w-full object-cover pointer-events-none`}
                  alt=""
                >
                </img>
                
                <div className={`${screenGuideType === 'desktop' ? 'flex w-1/2 h-1/2 bottom-[-10%] left-[5%]' : 'flex flex-col h-1/3 w-2/3 bottom-[5%] left-[15%]'} absolute overflow-hidden items-center gap-[5%] pointer-events-none`}>
                  <div className={`${screenGuideType === 'desktop' ? 'opacity-100 delay-75 w-[33%]' : 'opacity-0'} rounded-full bg-black/10 border-2 border-neutral-500/40 backdrop-blur-xs h-full transition-opacity`}>
                  </div>
                  <div className={`${screenGuideType === 'desktop' ? 'h-2/8' : 'h-3/9'} flex flex-col gap-2 w-[60%]`}>
                    <div className="bg-white/20 shadow-sm rounded-full w-full h-[50%]"></div>
                    <div className="bg-white/20 shadow-sm rounded-full w-2/3 h-[50%]"></div>
                  </div>
                </div>
                
                <span className="top-[5%] right-[2%] absolute bg-black/50 backdrop-blur-sm px-1.5 py-0.5 rounded-sm font-mono text-xs pointer-events-none">
                  {screenGuideType === 'desktop' ? '1400px View' : 'Mobile View'}
                </span>
              </div>
            </div>

            <input
              type='file'
              name='profile_banner'
              id='profile_banner'
              accept="image/png, image/jpeg, image/heic, image/heif"
              className="hidden"
              onChange={handleProfileBannerFileChange}
            ></input>
            
            <span className={`${editProfileFormTinyText} text-center`} id="banner-help-text">
              Safe Zone: Keep important details near the center to ensure visibility on all devices. Maximum size: 2560 x 1440
            </span>
          </div>

          {/* Username */}
          <div className='flex flex-col gap-2 w-full'>
            <label htmlFor='username' className={`${editProfileFormLabelStyle} text-base`}>Username</label>
            <input
              className={`${cn(editProfileFormContainerStyle, `${usernameIndicator && 'dark:border-red-800 border-red-800 transition-colors ease-in-out'}`)} outline-none p-3 dark:text-white text-black lowercase`}
              type='text'
              name='username'
              id='username'
              defaultValue={username}
              maxLength={30}
              minLength={1}
              onChange={usernameIndicatorHander}
              aria-describedby="username-help"
              aria-invalid={usernameIndicator ? "true" : "false"}
            ></input>
            
            <span 
              id="username-help" 
              className={`${cn(editProfileFormTinyText, `${usernameIndicator && 'dark:text-red-800 text-red-800 transition-colors ease-in-out'}`)}`}
            >
              Username can only contain letters, numbers, periods, and underscores. Max characters {charCounterUsername}/30
            </span>
          </div>

          {/* Bio */}
          <div className='flex flex-col gap-2 w-full'>
            <label htmlFor='bio' className={`${editProfileFormLabelStyle} text-base`}>Bio</label>
            <textarea
              className={`${editProfileFormContainerStyle} h-40 wrap-break-word p-3 dark:text-white text-black lowercase`}
              name='bio'
              id='bio'
              defaultValue={bio}
              maxLength={150}
              onChange={charCounterBioDisplayHandler}
              aria-describedby="bio-counter"
            ></textarea>
            
            <span 
              id="bio-counter" 
              className={`${editProfileFormTinyText}`} 
              aria-live="polite"
            >
              Max characters: {charCounterBio}/150
            </span>
          </div>

          {/* Actions */}
          <div className="flex gap-8 mb-8 w-full">
            <button 
              type="button" 
              className="bg-charcoal hover:shadow-md p-3 border border-border-color-dark rounded-md w-1/2 cursor-pointer" 
              onClick={() => setShowModal(false)}
            >
              Cancel
            </button>
            <SubmitButton/>
          </div>
        </form>
      </section>
    </Modal>
  )
}