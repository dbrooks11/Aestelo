import './App.css'
import { Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'
import SignupPage from './pages/SignupPage'
import LoginPage from './pages/LoginPage'
import ProfilePage from './pages/ProfilePage'
import FeedPage from './pages/FeedPage'


function App() {

  return (
      <Routes>
        <Route path='/' element={<HomePage />}/>
        <Route path="/signup" element={<SignupPage/>}/>
        <Route path='/login-email' element={<LoginPage isEmail={true} />}/>
        <Route path='/login-username' element={<LoginPage isEmail={false} />}/>
        <Route path='/profile/me' element={<ProfilePage/>}/>
        <Route path='/profile/:id' element={<ProfilePage/>}/>
        <Route path='/post/feed' element={<FeedPage/>}/>
      </Routes>
  )
}

export default App
