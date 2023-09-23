import React from 'react';
import FileManager from './components/FileManager';
import LoginPage from './Pages/LoginPage';
import { BrowserRouter, Route, Routes} from "react-router-dom";
import {Container} from "@mui/material";

function App() {
  return (
    // <BrowserRouter basename="/" >
    //         <Container
    //             maxWidth={false} disableGutters
    //             // sx={{width:'100%',border:"2px solid gray"}}

    //         >

    //             {/*<MainTitle/>*/}

    //             <Routes>
    //                 {/* <Route exact path={'/'} element={<UnauthorizedPage/>}/> */}
    //                 <Route exact path={'/'} element={<LoginPage/>}/>
    //                 {/* <Route exact path={'/register'} element={<RegisterPage/>}/> */}
    //                 <Route exact path={'/main'} element={<FileManager/>}/>
    //             </Routes>

    //         </Container>


    //     </BrowserRouter>
    <FileManager/>
  );
}

export default App;
