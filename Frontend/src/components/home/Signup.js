import React, { useState } from 'react'
import { NavLink, Navigate } from 'react-router-dom'
import { Button, Form, Grid, Segment, Message, Header } from 'semantic-ui-react'
import { useAuth } from '../context/AuthContext'
import { WorkApi } from '../misc/WorkApi'
import { parseJwt, handleLogError } from '../misc/Helpers'
import { motion } from 'framer-motion'

function Signup() {
  const Auth = useAuth()
  const isLoggedIn = Auth.userIsAuthenticated()

  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [isError, setIsError] = useState(false)
  const [errorMessage, setErrorMessage] = useState('')

  const handleInputChange = (e, { name, value }) => {
    if (name === 'username') {
      setUsername(value)
    } else if (name === 'password') {
      setPassword(value)
    } else if (name === 'name') {
      setName(value)
    } else if (name === 'email') {
      setEmail(value)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!(username && password && name && email)) {
      setIsError(true)
      setErrorMessage('Please, inform all fields!')
      return
    }

    const user = { username, password, name, email }

    try {
      const response = await WorkApi.signup(user)
      const { accessToken } = response.data
      const data = parseJwt(accessToken)
      const authenticatedUser = { data, accessToken }

      Auth.userLogin(authenticatedUser)

      setUsername('')
      setPassword('')
      setIsError(false)
      setErrorMessage('')
    } catch (error) {
      handleLogError(error)
      if (error.response && error.response.data) {
        const errorData = error.response.data
        let errorMessage = 'Invalid fields'
        if (errorData.status === 409) {
          errorMessage = errorData.message
        } else if (errorData.status === 400) {
          errorMessage = errorData.errors[0].defaultMessage
        }
        setIsError(true)
        setErrorMessage(errorMessage)
      }
    }
  }

  if (isLoggedIn) {
    return <Navigate to='/' />
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Grid textAlign='center' style={{ marginTop: '7em' }}>
        <Grid.Column style={{ maxWidth: 550 }}>
          <Form size='large' onSubmit={handleSubmit}>
            <Segment padded='very' className="glass-morphism">
              <Header as='h2' color='purple' textAlign='center' style={{ marginBottom: '2em' }}>
                Create New Account
              </Header>
              <Form.Input
                fluid
                autoFocus
                name='username'
                icon='user'
                iconPosition='left'
                placeholder='Username'
                onChange={handleInputChange}
                style={{ marginBottom: '1.5em' }}
                className="input-animation"
              />
              <Form.Input
                fluid
                name='password'
                icon='lock'
                iconPosition='left'
                placeholder='Password'
                type='password'
                onChange={handleInputChange}
                style={{ marginBottom: '1.5em' }}
                className="input-animation"
              />
              <Form.Input
                fluid
                name='name'
                icon='address card'
                iconPosition='left'
                placeholder='Name'
                onChange={handleInputChange}
                style={{ marginBottom: '1.5em' }}
                className="input-animation"
              />
              <Form.Input
                fluid
                name='email'
                icon='at'
                iconPosition='left'
                placeholder='Email'
                onChange={handleInputChange}
                style={{ marginBottom: '2em' }}
                className="input-animation"
              />
              <Button color='purple' fluid size='large'>Signup</Button>
            </Segment>
          </Form>
          <Message>{`Already have an account? `}
            <NavLink to="/login" color='purple'>Login</NavLink>
          </Message>
          {isError && <Message negative>{errorMessage}</Message>}
        </Grid.Column>
      </Grid>
    </motion.div>
  )
}

export default Signup