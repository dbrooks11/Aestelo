import { useState, useEffect,type Dispatch, type JSX, type SetStateAction, type ChangeEvent } from "react";
import cn from "../../util/tailwind_merger";
import { type ProfileDataType } from "../../pages/ProfilePage";
import { LoaderCircle, PencilLine, X } from 'lucide-react';
import { Monitor, Smartphone, Upload } from "lucide-react";
import { protectedInstance} from "../../util/axiosHelpers";
import { useFormStatus } from "react-dom";
import Modal from "../Modal";
import { useSpotMutation } from "../../hooks/SpotHooks/useSpotMutation";
import type { AxiosResponse } from "axios";
import axios from "axios";

type EditProfileFormProps = {
  profileBannerUrl: ProfileDataType['profile_banner']
  profilePhotoUrl: ProfileDataType['profile_photo']
  username: ProfileDataType['username']
  bio: ProfileDataType['bio']
  setProfileData: Dispatch<SetStateAction<ProfileDataType | null>>
  setShowModal: (value: boolean) => void
  showModal: boolean
}

// TODO: put the css back to respective elements
const editProfileFormScreenGuideButtonStyle = 'flex gap-2 py-1 px-2 items-center rounded-md hover:dark:text-text-main-dark hover:text-text-main-light cursor-pointer';
const editProfileFormScreenGuideButtonActiveStyle = 'dark:bg-bg-secondary-dark bg-bg-secondary-light dark:text-text-main-dark text-text-main-light shadow-sm';
const editProfileFormContainerStyle = 'border dark:bg-charcoal dark:border-border-color-dark bg-black/10 border-border-color-light rounded-lg text-sm';
const editProfileFormLabelStyle = 'font-bold dark:text-text-muted-dark text-text-main-light';
const editProfileFormTinyText = 'text-[10px] text-text-muted-light dark:text-text-muted-dark';

export default function EditProfileForm({
  username, bio, profilePhotoUrl, profileBannerUrl,
  setProfileData, setShowModal, showModal }: EditProfileFormProps): JSX.Element {
  
  const { updateAllSpotsInCache} = useSpotMutation();
  
  const [usernameIndicator, setUsernameIndictor] = useState<boolean>(false);
  const [charCounterBio, setCharCounterBio] = useState<number>(bio.length);
  const [charCounterUsername, setCharCounterUsername] = useState<number>(username.length);
  const [screenGuideType, setScreenGuideType] = useState<'mobile' | 'desktop'>('desktop');
  const [profilePhotoPreview, setProfilePhotoPreview] = useState<string | undefined>(undefined);
  const [profileBannerPreview, setProfileBannerPreview] = useState<string | undefined>(undefined);

  const handleProfileFileChange = (e: ChangeEvent<HTMLInputElement>, isFor: ('banner' | 'photo')) => {
    let tempUrl = '';
    const file = e.target.files;
    if(file && file.length === 1){
      if(isFor === 'photo'){
        if(profilePhotoPreview !== undefined) URL.revokeObjectURL(profilePhotoPreview);
        tempUrl = URL.createObjectURL(file[0]);
        setProfilePhotoPreview(tempUrl);
      }
      else if(isFor === 'banner'){
        if(profileBannerPreview !== undefined) URL.revokeObjectURL(profileBannerPreview);
        tempUrl = URL.createObjectURL(file[0]);
        setProfileBannerPreview(tempUrl);
      }
    }
  }


  useEffect(() => {
    return () => {
      if (profilePhotoPreview) {
        URL.revokeObjectURL(profilePhotoPreview);
        setProfilePhotoPreview(undefined);
      }
      if (profileBannerPreview) {
        URL.revokeObjectURL(profileBannerPreview);
        setProfileBannerPreview(undefined);
      }
    }
  },[])

  async function handleEditProfileFormClick(formData: FormData) {
    const files = new FormData();
    const info = new FormData();
  
    try {
      for (const [key, value] of formData.entries()){
        if (value instanceof File){
          if (value.size > 0){
            files.append(key, value);
          }
        }else{
          info.append(key, value);
        }
      }
        const response: AxiosResponse = await protectedInstance.post(`/s3/presigned-url/profile`, files);

        const presignedUrls = response.data.data;
        const fileArray: Array<[string, FormDataEntryValue]> = Array.from(files)
        console.log(fileArray)

        for (let i = 0; i < presignedUrls.length; i++){
          const { key, presigned_url } = presignedUrls[i]
          const fileData: [string, FormDataEntryValue] = fileArray[i]
          const file: File | string = fileData[1]
          
          if(file instanceof File){
            console.log("key:", key, "Presigned:", presigned_url)
            console.log("File", file, "File type", file.type)
            const responseS3 = await fetch(presigned_url, {
              method: "PUT",
              body: file,
              headers: {
                "Content-Type": file.type,
              }
            })
            console.log("Response S3:" , responseS3)
          }
        }  
    } catch(error) {
      console.log(error);
    }
  }

  //TODO: export submit button from signup or login an customize css
  function SubmitButton():JSX.Element{
    const {pending} = useFormStatus();
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

  const charCounterDisplayHandler = (e:ChangeEvent<HTMLInputElement | HTMLTextAreaElement>, isFor: ('username' | 'bio')) => {
    if(isFor === 'username'){
      const length = e.target.value.length;
      setCharCounterUsername(length);
    }
    else if(isFor === 'bio'){
      const length = e.target.value.length;
      setCharCounterBio(length);
    }
  }

  const usernameIndicatorHander = (e: ChangeEvent<HTMLInputElement>) => {
    const usernameChars = e.target.value;
    const re = /^[0-9A-Za-z_.]+$/;

    if(e.target.value === '' || !re.test(usernameChars)){
      setUsernameIndictor(true);
    }else{
      setUsernameIndictor(false);
    }

    charCounterDisplayHandler(e, 'username');
  }


  return (   
    <Modal 
      showModal={showModal} 
      closeModal={() => setShowModal(false)}
      dialogClassName="px-4"
    >
      
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
          <div className='flex items-center gap-[10%] md:gap-45 mt-6 w-full'>
            <label htmlFor='profile_photo' className={editProfileFormLabelStyle}>Profile Picture</label>
            
            <div className={cn(`${editProfileFormContainerStyle} relative`, 'rounded-full')}>
              <div className="w-30 h-30 md:w-35 md:h-35">
                <img
                  src={profilePhotoPreview ? profilePhotoPreview : profilePhotoUrl}
                  className='rounded-full w-full h-full object-cover pointer-events-none'
                  alt="Profile Picture Preview"
                ></img>
                <label 
                  htmlFor='profile_photo' 
                  className='bottom-0 right-1 absolute bg-black/15 dark:bg-white/10 backdrop-blur-sm p-2 rounded-full w-9 cursor-pointer'
                  aria-label="Change Profile Picture Button"
                >
                  <PencilLine className='w-full h-full' strokeWidth={1} aria-hidden="true" />
                </label>
              </div>
            </div>

            <input
              type='file'
              name='profile_photo'
              id='profile_photo'
              className='hidden'
              accept='image/*'
              onChange={(e) => handleProfileFileChange(e, 'photo')}
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
                <Upload size={20} aria-hidden="true" /> Change Banner
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
                  src={profileBannerPreview ? profileBannerPreview : profileBannerUrl}
                  className={`${screenGuideType === 'desktop' && 'object-[10%_52%]'} h-full w-full object-cover pointer-events-none`}
                  alt="Profile Banner Preview"
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
              accept="image/*"
              className="hidden"
              onChange={(e) => handleProfileFileChange(e, 'banner')}
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
              onChange={(e) => charCounterDisplayHandler(e, 'bio')}
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