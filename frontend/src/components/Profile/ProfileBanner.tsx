
import type {JSX} from 'react'

export default function ProfileBanner({profileBanner}: {profileBanner: string}): JSX.Element {
  return (
    <div className='absolute z-10 w-full pointer-events-none h-94 md:h-100 lg:h-100'>
      <img src={profileBanner} className='mask-b-from-75% mask-b-to-99% md:mask-b-from-70% md:mask-b-to-95% object-cover object-[0%_70%] md:object-[5%_48%] w-full h-full'></img>
    </div>
  )
}
