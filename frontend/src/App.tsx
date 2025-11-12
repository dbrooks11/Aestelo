import './App.css'
import { Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import SignupPage from './pages/SignupPage'


function App() {

  return (
    <>
      <Routes>
        <Route path='/' element={<HomePage />}/>
        <Route path="/signup" element={<SignupPage/>}/>
        <Route path='/login-email' element={<LoginPage />}/>
      </Routes>
    </>
  )
}

export default App
