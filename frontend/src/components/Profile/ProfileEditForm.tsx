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

            {/* Upload Banner Section */}
            <div className="w-full flex flex-col gap-4 mt-4">
              {/* Upload Banner Header */}
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
                  className={`${screenGuideType === 'desktop' ? 'w-full aspect-3/1': 'w-100 aspect-15/16'} border-4 border-black bg-black rounded-lg overflow-hidden transition-all relative`}
                  >
                  <img src={myProfilePic} 
                    className="h-full w-full object-cover pointer-events-none"
                    alt="Banner Preview"
                  >
                  </img>
                  <div className="absolute top-[60%] left-[5%] flex overflow-hidden items-center gap-[5%] pointer-events-none w-1/2 h-1/2" aria-hidden>
                    <div className="rounded-full  bg-black/10 border-2 border-neutral-500/40 backdrop-blur-xs h-full w-[33%]">
                      <div className="absolute rounded-full top-[30%] bg-black">
                      </div>
                    </div>
                    <div className="flex flex-col gap-2 w-[60%] h-2/8">
                      <div className="w-full h-[50%] rounded-full bg-white/20 shadow-sm"></div>
                      <div className="w-2/3 h-[50%] rounded-full bg-white/20 shadow-sm"></div>
                    </div>
                  </div>
                  <span className="absolute top-[5%] right-[2%] bg-black/50 backdrop-blur-sm px-1.5 py-0.5 text-xs rounded-sm font-mono">1200px View</span>
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