import {type JSX} from 'react'
import { Tabs, Tab } from '../Tabs'
import { MapPin, Map, MapPinned, BookMarked } from 'lucide-react'

export default function ProfileTabs(): JSX.Element {

  


  return (
      <Tabs>
        <Tab label={'Posts'} icon={<MapPin/>}>
          <p>Post says hello</p>
        </Tab>
        <Tab label={'Visits'} icon={<MapPinned/>}>
          <p>Visits says goodbye</p>
        </Tab>
        <Tab label={'Saved'} icon={<BookMarked/>}>
          <p>Saved says adios</p>
        </Tab>
        <Tab label={'Map'} icon={<Map/>}>
          <p>Map says rawr</p>
        </Tab>
      </Tabs>
  )
}
