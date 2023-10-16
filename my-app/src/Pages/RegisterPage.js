import React, { useState, useEffect } from 'react';
import { Button, Container, Grid, Paper, TextField, Typography, Box } from '@mui/material';
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom'; 
import { addUser, authUser } from '../store/UserSlice';

const RegisterPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [re_password, setRePassword] = useState('');
  const [passwordsMatch, setPasswordsMatch] = useState(true);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      navigate('/main');
    }
  }, [navigate]);

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handleRePasswordChange = (e) => {
    setRePassword(e.target.value);
    setPasswordsMatch(e.target.value === password);
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    if (password !== re_password) {
      setPasswordsMatch(false);
      return;
    }
    dispatch(addUser({
      username: email,
      password: password,
    })).then(() => {
      dispatch(authUser({
        username: email,
        password: password,
      })).then((response) => {
        const accessToken = response.payload.access;
        if (accessToken) {
          navigate('/main');
        }
      });
    });
    console.log('Submitted:', email, password);
  };
  
  return (
    <Container maxWidth="xs">
      <Paper elevation={3} sx={{ p: 4, mt: 8 }}>
        <Typography variant="h5" align="center" sx={{ mb: 4 }}>
          Регистрация
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
              <TextField
                error={!passwordsMatch}
                helperText={!passwordsMatch ? 'Пароли не совпадают' : ''}
                fullWidth
                label="Повторите пароль"
                type="password"
                variant="outlined"
                value={re_password}
                onChange={handleRePasswordChange}
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
      </Paper>
    </Container>
  );
};

export default RegisterPage;
