import { useState, type JSX } from "react";
import cn from "../../util/tailwind_merger";
import { type ProfileData } from "../../pages/ProfilePage";
import { PencilLine} from 'lucide-react'
import myProfilePic from '/src/assets/my_profile_pic.jpg' //TODO: remove profile pic (only for testing)
import { Monitor, Smartphone, Upload } from "lucide-react";

// TODO: add profile banner to form and props type once setup in backend

type EditProfileFormProps = {
  profile_photo: string
  username: string | undefined
  bio: string
  setProfileData: (data: ProfileData) => void
}

const editProfileFormSectionContainerStyle = ''
const editProfileFormScreenGuideButtonStyle ='flex gap-2 py-1 px-2 items-center rounded-md hover:dark:text-text-main-dark hover:text-text-main-light cursor-pointer'
const editProfileFormScreenGuideButtonActiveStyle = 'dark:bg-bg-secondary-dark bg-bg-secondary-light dark:text-text-main-dark text-text-main-light shadow-sm'
const editProfileFormContainerStyle ='border dark:bg-charcoal dark:border-border-color-dark bg-black/10 border-border-color-light rounded-lg text-sm'
const editProfileFormLabelStyle = 'dark:text-text-muted-dark text-text-muted-light font-bold'

//TODO: Set user banner from profile page to edit form state (same for profile)
//TODO: Set user profile_photo from profile page to edit form state (same for profile)

export default function EditProfileForm({username, bio, profile_photo, setProfileData}: EditProfileFormProps): JSX.Element {

    const [screenGuideType ,setScreenGuideType] = useState<'mobile' | 'desktop'>('desktop')


    const handleEditProfileFormClick = (formData) => {
      // TODO: set data for banner and profile
      const data = Object.fromEntries(formData)

      setProfileData((prev) => {
        return(
          {
            ...prev,
            username: data.username,
            bio: data.bio
          }
        )
      })
    }

    // TODO: Add api call to update profile on form submit

    return(
        <form action={handleEditProfileFormClick} className='flex flex-col flex-1 items-center gap-10 px-6 overflow-y-scroll text-white'>
            <div className=' mt-6 flex items-center gap-20 w-full'>
              <label  htmlFor='profile_photo' className={editProfileFormLabelStyle}>PROFILE PICTURE</label>
              <div className={cn(`${editProfileFormContainerStyle} relative sm:ml-15`, 'rounded-full')}>
                <img 
                src={profile_photo} 
                className='rounded-full w-35 h-35 object-cover pointer-events-none'
                alt="Profile Picture Preview"
                ></img>
                <label htmlFor='profile_photo' className='top-25 left-25 p-2 absolute w-9 cursor-pointer rounded-full bg-white/10 backdrop-blur-sm'><PencilLine className='w-full h-full' strokeWidth={1}/></label>
              </div>
              <input aria-hidden type='file' name='profile_photo' id='profile_photo' className='hidden' accept='image/png, image/jpeg'></input>
            </div>

            {/* Upload Banner Section */}
            <div className="w-full flex flex-col gap-4 mt-4">
              {/* Upload Banner Header */}
              <div className="flex justify-between">
                <h2 className={editProfileFormLabelStyle}>PROFILE BANNER</h2>
                <label htmlFor="profile_banner" className="text-accents-primary text-sm flex items-center gap-2 cursor-pointer hover:underline"><Upload size={20}/>Change Image</label>
              </div>
              <div className={`${editProfileFormContainerStyle} w-50 flex justify-between border p-1 dark:text-text-muted-dark text-text-muted-light font-bold`}>
                <button 
                className={cn(editProfileFormScreenGuideButtonStyle, `${screenGuideType === 'desktop' ? editProfileFormScreenGuideButtonActiveStyle : null}`)}
                type="button"
                onClick={()=> setScreenGuideType('desktop')}
                >
                  <Monitor size={18}/>Desktop</button>
                <button 
                className={cn(editProfileFormScreenGuideButtonStyle, `${screenGuideType === 'mobile' ? editProfileFormScreenGuideButtonActiveStyle : null}`)}
                type="button"
                onClick={()=> setScreenGuideType('mobile')}
                >
                  <Smartphone size={18}/>Mobile
                </button>
              </div>
              <div className={`${editProfileFormContainerStyle} min-h-60 flex items-center justify-center w-full py-8`}>
                <div 
                  className={`${screenGuideType === 'desktop' ? 'w-full aspect-3/1': 'w-100 aspect-15/16'} border-4 border-black bg-black rounded-lg overflow-hidden transition-all relative shadow-lg`}
                  >
                  <img src={myProfilePic} 
                    className={`${screenGuideType === 'desktop' ? 'object-[10%_52%]' : null} h-full w-full object-cover  pointer-events-none"
                    alt="Banner Preview`}
                  >
                  </img>
                  <div className={`${screenGuideType === 'desktop' ? 'flex w-1/2 h-1/2 bottom-[-10%] left-[5%]' : 'flex flex-col h-1/3 w-2/3 bottom-[5%] left-[15%]'} absolute overflow-hidden items-center gap-[5%] pointer-events-none`} aria-hidden>
                    <div className={`${screenGuideType === 'desktop' ? 'opacity-100 delay-75 w-[33%]' : 'opacity-0'} rounded-full bg-black/10 border-2 border-neutral-500/40 backdrop-blur-xs h-full  transition-opacity`}>
                    </div>
                    <div className={`${screenGuideType === 'desktop' ? 'h-2/8': 'h-3/9'} flex flex-col gap-2 w-[60%]`}>
                      <div className="w-full h-[50%] rounded-full bg-white/20 shadow-sm"></div>
                      <div className="w-2/3 h-[50%] rounded-full bg-white/20 shadow-sm"></div>
                    </div>
                  </div>
                  <span className="absolute top-[5%] right-[2%] bg-black/50 backdrop-blur-sm px-1.5 py-0.5 text-xs rounded-sm font-mono pointer-events-none">{screenGuideType === 'desktop' ? '1200px View' : 'Mobile View'}</span>
                </div>
              </div>
              <input type='file' name='profile_banner' id='profile_banner' accept="image/png, image/jpeg" className="hidden"></input>
              <span className="text-[10px] text-center dark:text-text-muted-dark text-text-muted-light">Safe Zone: Keep important details near the center to ensure visibility on all devices.</span>
            </div>
            <div className='flex flex-col w-full gap-2'>
              <label htmlFor='username' className={`${editProfileFormLabelStyle} text-base`}>Username</label>
              <input 
              className={`${editProfileFormContainerStyle} p-3`} 
              type='text' 
              name='username' 
              id='username'
              defaultValue={username}
              ></input>
            </div>
            <div className='flex flex-col w-full gap-2'>
              <label htmlFor='bio' className={`${editProfileFormLabelStyle} text-base`}>Bio</label>
              <textarea 
              className={`${editProfileFormContainerStyle} h-40 wrap-break-word p-3`}  
              name='bio' 
              id='bio'
              defaultValue={bio}
              ></textarea>
            </div>
          <button type='submit'>Confirm</button>
        </form>
    )
}