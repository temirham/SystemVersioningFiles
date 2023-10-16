import { useNavigate } from 'react-router-dom';
import {Container, Typography, Button, Grid} from "@mui/material";
function UnauthorizedPage() {
    const navigate = useNavigate();
    function handleClick() {
        navigate('/login');
    }
    return(
        <>
        <Container maxWidth={'sm'}
        sx={{backgroundColor:'secondary.semitransparent', marginTop:4, paddingY: '40px', width:'400px', borderRadius: '20px',}}
        >

            <Grid
              container
              direction="column"
              justifyContent="center"
              alignItems="center"
            >
            <Typography variant={'h4'} align={'center'} paragraph
            sx={{fontFamily:"NunitoSansExtraLightFont", color:"text.text2"}}
            >
                Приветствуем Вас на сервисе облачных заметок!
            </Typography>
            <Button variant={"contained"} align={'center'} onClick={handleClick}
            sx={{backgroundColor:'secondary.button', fontFamily:'GenshinFont', margin: '50px 30px', padding: '20px 100px', borderRadius: '26px'}}
            >Вход</Button>
            </Grid>
        </Container>
            </>
    )

}

export default UnauthorizedPage;

