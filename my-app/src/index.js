import React from 'react';
import ReactDOM from 'react-dom';

import { Provider } from 'react-redux';
import store from '/Users/temirhanmamaev/Documents/test_front/my-app/src/store/store.js'; 
import { CssBaseline, ThemeProvider, createTheme } from '@mui/material';
import App from './App';

// Создаем пользовательскую тему Material-UI
const theme = createTheme({
  palette: {
    mode: 'light', // Вы можете установить 'dark' вместо 'light', если хотите темную тему
  },
});

ReactDOM.render(
  // <React.StrictMode>
    <Provider store={store}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <App />
      </ThemeProvider>
    </Provider>,
    
  // </React.StrictMode>,
  document.getElementById('root')
);
