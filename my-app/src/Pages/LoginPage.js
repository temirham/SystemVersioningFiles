import React, { useState, useEffect } from 'react';
import { Box, Button, Container, Grid, Paper, TextField, Typography } from '@mui/material';
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom'; 
import { authUser } from '../store/UserSlice';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    dispatch(authUser({
      username: email,
      password: password,
    })).then((response) => {
      const accessToken = response.payload.access;
      if (accessToken) {
        navigate('/main'); 
      }
    });
    console.log('Submitted:', email, password);
  };

  const handleRegisterClick = () => {
    navigate('/register');
  };

  return (
    <Container maxWidth="xs">
      <Paper elevation={3} sx={{ p: 4, mt: 8 }}>
        <Typography variant="h5" align="center" sx={{ mb: 4 }}>
          Авторизация
        </Typography>
        <form onSubmit={handleFormSubmit}>
          <Grid container direction="column" spacing={2}>
            <Grid item>
              <TextField
                fullWidth
                label="Логин"
                variant="outlined"
                value={email}
                onChange={handleEmailChange}
              />
            </Grid>
            <Grid item>
              <TextField
                fullWidth
                label="Пароль"
                type="password"
                variant="outlined"
                value={password}
                onChange={handlePasswordChange}
              />
            </Grid>
            <Grid item>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                fullWidth
                size="large"
              >
                Войти
              </Button>
            </Grid>
          </Grid>
        </form>
        <Box textAlign="center" mt={2}>
          <Button color="primary" onClick={handleRegisterClick}>Нет аккаунта?</Button>
        </Box>
      </Paper>
    </Container>
  );
};

export default LoginPage;
