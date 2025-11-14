
import {type JSX, useState, useEffect} from 'react'
import { AxisErrorHelper, protectedInstance } from '../util/axios_api_helpers'

export default function FeedPage(): JSX.Element {

    const [feed, setFeed] = useState<null>(null)
    const [isLoading, setIsLoading] = useState<boolean>(true)
    const [error, setError] = useState<string | null>("")


    useEffect(() => {
        async function getFeed(){
            try{
                const response = await protectedInstance.get('/post/feed')

                const data = response.data

                if(response.status === 200){
                    setFeed(data)
                }
            }catch(error){
                AxisErrorHelper(error, setError, "Feed")
            }finally{
                setIsLoading(false)
            }
        }

        getFeed()
    }, []);

    console.log(feed)
        
      
  return (
    <main>
        {!isLoading ? "hello" : "Loading feed..."}
    </main>
  )
}
