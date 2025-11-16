import { Routes, Route, useLocation } from 'react-router-dom'
import { useState, useEffect} from 'react'
import Header from './components/Header'
import HomePage from './pages/HomePage'
import SignupPage from './pages/SignupPage'
import LoginPage from './pages/LoginPage'
import ProfilePage from './pages/ProfilePage'
import FeedPage from './pages/FeedPage'



function App() {

  const currentRoute = useLocation()
  const hideHeaderRoutes = ['/','/signup','/login-email','/login-username']

  const [theme, setTheme] = useState<'light' | 'dark'>(() => (localStorage.getItem("theme") as "light" | "dark") ?? "light")
  
  useEffect(() => {
      localStorage.setItem('theme', theme)
  }, [theme]);


  return (
    <div data-theme={theme} className="h-screen bg-bg-light-secondary dark:bg-charcoal">
      <Header 
      isAuthenticated={hideHeaderRoutes.includes(currentRoute.pathname) ? false : true} 
      setTheme={setTheme}
      theme={theme}
      ></Header>
      <Routes>
        <Route path='/' element={<HomePage />}/>
        <Route path="/signup" element={<SignupPage/>}/>
        <Route path='/login-email' element={<LoginPage isEmail={true} />}/>
        <Route path='/login-username' element={<LoginPage isEmail={false} />}/>
        <Route path='/profile/me' element={<ProfilePage/>}/>
        <Route path='/profile/:id' element={<ProfilePage/>}/>
        <Route path='/post/feed' element={<FeedPage/>}/>
      </Routes>
    </div>
  )
}

export default App
