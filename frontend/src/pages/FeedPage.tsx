
import {type JSX, useState, useEffect} from 'react'
import { AxiosErrorHelper, protectedInstance } from '../util/axios_api_helpers'
import toast, { Toaster } from 'react-hot-toast'
import Post from '../components/ContentType/Spot/Spot'
import Spot from '../components/ContentType/Spot/Spot'

export default function FeedPage(): JSX.Element {

    const [feed, setFeed] = useState<null>(null)
    const [isLoading, setIsLoading] = useState<boolean>(false)
    const [error, setError] = useState<string | null>("")


    // useEffect(() => {
    //     async function getFeed(){
    //         try{
    //             const response = await protectedInstance.get('/post/feed')

    //             const data = response.data

    //             if(response.status === 200){
    //                 setFeed(data)
    //             }
    //         }catch(error){
    //             const newError = AxiosErrorHelper(error)
    //             toast.error(newError, {
    //                 toasterId: 'feed'
    //             })
    //         }finally{
    //             setIsLoading(false)
    //         }
    //     }

    //     getFeed()
    // }, []);

    // console.log(feed)
        
      
  return (
    <main>
        {!isLoading ? 
            <div>hello</div>

        : "Loading feed..."}
        <Toaster toasterId='feed'/>
    </main>
  )
}
