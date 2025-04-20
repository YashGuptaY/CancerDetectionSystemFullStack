import { Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import PredictionForm from './PredictionForm'

function UserPage() {
  const Auth = useAuth()
  const user = Auth.getUser()
  const isUser = user.data.rol[0] === 'USER'

  if (!isUser) {
    return <Navigate to='/' />
  }

  return (
    <div>
      <PredictionForm />
    </div>
  )
}

export default UserPage