import { useState, type JSX } from "react";
import cn from "../../util/tailwind_merger";
import { PencilLine} from 'lucide-react'
import myProfilePic from '/src/assets/my_profile_pic.jpg' //TODO: remove profile pic (only for testing)
import { Monitor, Smartphone, Upload } from "lucide-react";


type EditProfileFormProps = {

}

const editProfileFormSectionContainerStyle = ''
const editProfileFormScreenGuideButtonStyle ='flex gap-2 py-1 px-2 items-center rounded-md hover:dark:text-text-main-dark hover:text-text-main-light cursor-pointer'
const editProfileFormScreenGuideButtonActiveStyle = 'dark:bg-bg-secondary-dark bg-bg-secondary-light dark:text-text-main-dark text-text-main-light'
const editProfileFormContainerStyle ='border dark:bg-charcoal dark:border-border-color-dark bg-accents-subtle border-border-color-light rounded-lg text-sm'

//TODO: Set user banner from profile page to edit form state (same for profile)

export default function EditProfileForm(): JSX.Element {

    const [screenGuideType ,setScreenGuideType] = useState<'mobile' | 'desktop'>('desktop')

    return(
        <form className='flex flex-col flex-1 items-center gap-30 px-6 overflow-y-scroll text-white'>
            {/* <div className=' mt-6 flex items-center gap-20 w-full'>
              <h2 className='justify-start'>Profile Picture</h2>
              <div className='relative'>
                <img 
                src={myProfilePic} 
                className='rounded-full w-35 h-35 object-cover pointer-events-none'
                alt="Profile Picture Preview"
                ></img>
                <label htmlFor='profile_photo' className='top-25 left-25 p-2 absolute w-9 cursor-pointer rounded-full bg-white/10 backdrop-blur-sm'><PencilLine className='w-full h-full' strokeWidth={1}/></label>
              </div>
              <input aria-hidden type='file' name='profile_photo' id='profile_photo' className='hidden' accept='image/png, image/jpeg'></input>
            </div> */}
            <div className="w-full flex flex-col gap-4 mt-4">
              <div className="flex justify-between">
                <h2 className="dark:text-text-muted-dark text-text-muted-light font-bold">PROFILE BANNER</h2>
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
                className={`${screenGuideType === 'desktop' ? 'w-full aspect-3/1': 'w-100 aspect-15/16'} border-4 border-black bg-black rounded-lg overflow-hidden transition-all `}
                >
                  <img src={myProfilePic} 
                  className="h-full w-full object-cover pointer-events-none"
                  alt="Banner Preview"
                  ></img>
                </div>
              </div>
              <input type='file' name='profile_banner' id='profile_banner' accept="image/png, image/jpeg" className="hidden"></input>
            </div>
            {/* <div className='flex justify-between mt-4 p-4 w-150 text-lg'>
              <label htmlFor='username'>Username</label>
              <input type='text' name='username' id='username'></input>
            </div>
            <div>
              <label htmlFor='bio'>Bio</label>
              <input type='text' name='bio' id='bio'></input>
            </div> */}
          <button type='submit'>Confirm</button>
        </form>
    )
}