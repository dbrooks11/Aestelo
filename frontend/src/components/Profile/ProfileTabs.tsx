import {type JSX} from 'react'
import { Tabs, Tab } from '../Tabs'
import { MapPin, Map, MapPinned, BookMarked } from 'lucide-react'



export default function ProfileTabs(): JSX.Element {

  return (
      <Tabs 
      tabsAndContentContainerStyle='w-full mt-12'
      tabsContainerStyle='sticky top-16 dark:bg-charcoal/65 bg-white/65 backdrop-blur-lg '
      activeTabStyle='dark:text-white text-accents-deep border-b-2 border-b-accents-primary'
      tabsStyle='dark:text-neutral-500 font-bold hover:dark:text-white hover:text-accents-deep'
      >
        <Tab label={'Posts'} icon={<MapPin className='md:hidden'/>}>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
          <p>Post says hello</p>
        </Tab>
        <Tab label={'Visits'} icon={<MapPinned className='md:hidden'/>}>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
          <p>Visits says goodbye</p>
        </Tab>
        <Tab label={'Saved'} icon={<BookMarked className='md:hidden'/>}>
          <p>Saved says adios</p>
        </Tab>
        <Tab label={'Map'} icon={<Map className='md:hidden'/>}>
          <p>Map says rawr</p>
        </Tab>
      </Tabs>
  )
}
