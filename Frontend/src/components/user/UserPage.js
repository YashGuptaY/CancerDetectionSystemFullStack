import React from 'react'
import { Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import PredictionForm from './PredictionForm'

function UserPage() {
  const Auth = useAuth()
  const user = Auth.getUser()

  if (!user || !user.data) {
    return <Navigate to='/login' />
  }

  const userRole = user.data.rol[0]
  if (userRole !== 'USER') {
    return <Navigate to='/' />
  }

  return <PredictionForm />
}

export default UserPage