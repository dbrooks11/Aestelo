import { Routes, Route, useLocation, useNavigate, type NavigateFunction } from 'react-router-dom'
import { useState, useEffect} from 'react'
import Header from './components/Header'
import HomePage from './pages/HomePage'
import SignupPage from './pages/SignupPage'
import LoginPage from './pages/LoginPage'
import ProfilePage from './pages/ProfilePage'
import FeedPage from './pages/FeedPage'



function App() {
  const navigate: NavigateFunction = useNavigate()
  const currentRoute = useLocation()
  const hideHeaderRoutes = ['/','/about','/explore','/signup','/login-email','/login-username']

  const [theme, setTheme] = useState<'light' | 'dark'>(() => (localStorage.getItem("theme") as "light" | "dark") ?? "light")
  
  useEffect(() => {
      localStorage.setItem('theme', theme)
  }, [theme]);

  const [globalErrors, setGlobalErrors] = useState<number>(0)

  useEffect(() => {
    if(globalErrors in [401, 410, 403]){
      navigate('login-email')
    }else{
      return
    }
  }, [globalErrors]);


  return (
    <div data-theme={theme} className="flex flex-col h-screen bg-bg-light-secondary dark:bg-charcoal">
      <Header 
      isAuthenticated={hideHeaderRoutes.includes(currentRoute.pathname) ? false : true} 
      setTheme={setTheme}
      theme={theme}
      ></Header>
      <div className='flex-1 flex flex-col'>
        {/* TODO: channge route element for about and explore  */}
        <Routes>
          <Route path='/' element={<HomePage />}/>
          <Route path='/about' element={<HomePage/>}/>
          <Route path='/explore' element={<HomePage/>}/>
          <Route path="/signup" element={<SignupPage/>}/>
          <Route path='/login-email' element={<LoginPage isEmail={true} />}/>
          <Route path='/login-username' element={<LoginPage isEmail={false} />}/>
          <Route path='/profile/me' element={<ProfilePage setGlobalErrors={setGlobalErrors}/>}/>
          <Route path='/profile/:id' element={<ProfilePage setGlobalErrors={setGlobalErrors}/>}/>
          <Route path='/post/feed' element={<FeedPage/>}/>
        </Routes>
      </div>
    </div>
  )
}

export default App
