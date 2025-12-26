
import type {JSX} from 'react'


// TODO: fix bottom blending issue of banner

export default function ProfileBanner({profileBanner}: {profileBanner: string}): JSX.Element {
  return (
    <div className='z-10 absolute w-full h-94 md:h-100 lg:h-105 pointer-events-none'
      role="banner" 
    >
      <img src={profileBanner} className='mask-b-from-80% md:mask-b-from-85% mask-b-to-99% md:mask-b-to-95% w-full h-full object-[0%_70%] object-cover md:object-[5%_48%]'></img>
    </div>
  )
}
