import { Routes, Route } from 'react-router-dom'
import AuthProvider from './hooks/AuthProvider'
import { useTheme } from './context/ThemeContext'
import ProtectedRoute from './components/Wrappers/ProtectedRoute'
import PublicRoute from './components/Wrappers/PublicRoute'
import HomePage from './pages/HomePage'
import SignupPage from './pages/SignupPage'
import LoginPage from './pages/LoginPage'
import ProfilePage from './pages/ProfilePage'
import FeedPage from './pages/FeedPage'


function App() {
  const {theme} = useTheme()


  return (
    
      <div data-theme={theme} className="flex flex-col min-h-screen bg-bg-light-secondary dark:bg-charcoal">
        <AuthProvider>
        {/* TODO: channge route element for about and explore  */}
          <Routes>
            <Route element={<PublicRoute/>}>
              <Route path='/' element={<HomePage />}/>
              <Route path='/about' element={<HomePage/>}/>
              <Route path='/explore' element={<HomePage/>}/>
              <Route path="/signup" element={<SignupPage/>}/>
              <Route path='/login-email' element={<LoginPage isEmail={true}/>}/>
              <Route path='/login-username' element={<LoginPage isEmail={false}/>}/>
            </Route>

            <Route element={<ProtectedRoute/>}>
              <Route path='/profile/me' element={<ProfilePage/>}/>
              <Route path='/profile/:id' element={<ProfilePage/>}/>
              <Route path='/post/feed' element={<FeedPage/>}/>
            </Route>

            <Route path='*' element={<div>404 Page Not Found</div>}/>
          </Routes>
        </AuthProvider>
      </div>
  )
}

export default App
