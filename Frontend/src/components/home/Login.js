import React, { useState } from 'react'
import { NavLink, Navigate } from 'react-router-dom'
import { Button, Form, Grid, Icon, Segment, Menu, Message, Divider, Header } from 'semantic-ui-react'
import { useAuth } from '../context/AuthContext'
import { WorkApi } from '../misc/WorkApi'
import { parseJwt, getSocialLoginUrl, handleLogError } from '../misc/Helpers'
import { motion } from 'framer-motion'

function Login() {
  const Auth = useAuth()
  const isLoggedIn = Auth.userIsAuthenticated()

  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [isError, setIsError] = useState(false)

  const handleInputChange = (e, { name, value }) => {
    if (name === 'username') {
      setUsername(value)
    } else if (name === 'password') {
      setPassword(value)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!(username && password)) {
      setIsError(true)
      return
    }

    try {
      const response = await WorkApi.authenticate(username, password)
      const { accessToken } = response.data
      const data = parseJwt(accessToken)
      const authenticatedUser = { data, accessToken }

      Auth.userLogin(authenticatedUser)

      setUsername('')
      setPassword('')
      setIsError(false)
    } catch (error) {
      handleLogError(error)
      setIsError(true)
    }
  }

  if (isLoggedIn) {
    const user = Auth.getUser()
    const userRole = user.data.rol[0]
    return <Navigate to={userRole === 'ADMIN' ? '/adminpage' : '/userpage'} />
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
                Login to your account
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
                style={{ marginBottom: '2em' }}
                className="input-animation"
              />
              <Button color='purple' fluid size='large'>Login</Button>
            </Segment>
          </Form>
          <Message>
            Don't have an account?{' '}
            <NavLink to="/signup" style={{ color: 'purple' }}>
              Sign Up
            </NavLink>
          </Message>
          {isError && <Message negative>The username or password provided are incorrect!</Message>}

          <Divider horizontal>or connect with</Divider>

          <Menu compact icon='labeled'>
            <Menu.Item name='github' href={getSocialLoginUrl('github')}>
              <Icon name='github' />Github
            </Menu.Item>
            <Menu.Item name='google' href={getSocialLoginUrl('google')}>
              <Icon name='google' />Google
            </Menu.Item>
            <Menu.Item name='facebook'>
              <Icon name='facebook' disabled />Facebook
            </Menu.Item>
            <Menu.Item name='instagram'>
              <Icon name='instagram' disabled />Instagram
            </Menu.Item>
          </Menu>
        </Grid.Column>
      </Grid>
    </motion.div>
  )
}

export default Login
