import {type JSX} from 'react'
import { Tabs, Tab } from '../Tabs'
import { MapPin, Map, MapPinned, BookMarked } from 'lucide-react'
import FetchSpots from './DataFetching/FetchSpots'
import FetchCollections from './DataFetching/FetchCollections'

export default function ProfileTabs(): JSX.Element {

  

  return (
      <Tabs 
      tabsAndContentContainerStyle='w-full mt-12'
      tabsContainerStyle='sticky top-16 dark:bg-charcoal/65 bg-bg-light-secondary/65 backdrop-blur-lg z-30 border-b dark:border-white/5 border-black/5'
      activeTabStyle='dark:text-white text-accents-deep border-b-2 border-b-accents-primary'
      tabsStyle='dark:text-neutral-500 font-bold hover:dark:text-white hover:text-accents-deep'
      >
        <Tab label={'Spots'} icon={<MapPin className='md:hidden'/>}>
          <FetchSpots/>
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
          <FetchCollections/>
        </Tab>
        <Tab label={'Map'} icon={<Map className='md:hidden'/>}>
          <p>Map says rawr</p>
        </Tab>
      </Tabs>
  )
}
