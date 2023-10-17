import './App.css';
import { BrowserRouter, Route, Routes} from "react-router-dom";
import UnauthorizedPage from "./Pages/UnauthorizedPage";
import LoginPage from "./Pages/LoginPage";
import RegisterPage from "./Pages/RegisterPage";
import {Container} from "@mui/material";
import FileManager from './components/FileManager';

function App() {
  return (
      // <DocumentTitle title={'Notes'}>
        <BrowserRouter basename="/" >
            <Container
                maxWidth={false} disableGutters

            >

                <Routes>
                    <Route exact path={'/'} element={<UnauthorizedPage/>}/>
                    <Route exact path={'/login'} element={<LoginPage/>}/>
                    <Route exact path={'/register'} element={<RegisterPage/>}/>
                    <Route exact path={'/main'} element={<FileManager/>}/>
                </Routes>

            </Container>


        </BrowserRouter>
  );
}

export default App;
