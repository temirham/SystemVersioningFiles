import React from 'react';
import FileManager from '../components/FileManager.js';

import { Button, Container, Typography, Grid} from '@mui/material';
import { useNavigate } from 'react-router-dom';

function MainPage() {
    const navigate = useNavigate();

    function handleClick() {
        navigate('/login');
    }
  return (
    <Container>
      {localStorage.getItem('accessToken') ? (
        <FileManager />
      ) : (
        <div 
            style={{
                marginTop: '200px'
            }}
        >
            <Container 
                className="background-animation"
                sx={{ 
                    marginTop: 4, 
                    paddingY: '40px', 
                    width: '400px', 
                    borderRadius: '20px',
                }}
            >
                <Grid
                    
                >
                    <Typography 
                        variant={'h4'} 
                        align={'center'} 
                    >
                        Вы не вошли в систему
                    </Typography>
                    <Button 
                        variant={"contained"} 
                        align={'center'} 
                        onClick={handleClick}
                        sx={{
                            backgroundColor: 'secondary.button', 
                            marginTop: '50px', 
                            padding: '20px 100px', 
                            borderRadius: '26px'
                        }}
                    >
                        Авторизоваться
                    </Button>
                </Grid>
            </Container>
            </div>
      )}
    </Container>
  );
}

export default MainPage;
