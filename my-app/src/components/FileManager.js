import React, { useState, useEffect} from 'react';
import FileUploader from './FileUploader';
import {useDispatch, useSelector} from "react-redux";
import FileCard from './FileCard'; // Импортируйте компонент FileCard
import { uploadFile } from '/Users/temirhanmamaev/Documents/test_front/my-app/src/store/fileSlice.js';
 
import {
  Button,
  Typography,
  Grid,
  Container,
  Paper,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Drawer,
  AppBar,
  Toolbar,
} from '@mui/material';
import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';
import ImageIcon from '@mui/icons-material/Image';
import DescriptionIcon from '@mui/icons-material/Description';
import FolderIcon from '@mui/icons-material/Folder';
import MenuIcon from '@mui/icons-material/Menu';
import {getUser, refreshUser} from "../store/UserSlice";
import { addFile, getUserFile, loadFiles } from '../store/fileSlice';
import { GetFiles } from '/Users/temirhanmamaev/Documents/test_front/my-app/src/Function/GetFiles.js';


  

function FileManager() {
  const [isDrawerOpen, setDrawerOpen] = useState(false);
  const [selectedMenu, setSelectedMenu] = useState('mydrive'); // Начальное значение выбора

  const handleMenuClick = (menu) => {
    setSelectedMenu(menu);
  };
  const dispatch = useDispatch();
//   dispatch(loadFiles());
  const {userId} = useSelector((state) => state.userId);
  const {username} = useSelector((state) => state.username);
  const {files} = useSelector((state) => state.files); // Замените на ваш собственный селектор для списка файлов
  useEffect(() => {
    const fetchData = async () => {
        await dispatch(loadFiles());
    }
    fetchData()
  }, [])
//   GetFiles()
  const handleFileUpload = (selectedFile) => {
    if (selectedFile) {
        dispatch(uploadFile({ file: selectedFile, userId }));
      }
  };

  return (
    <Container style={{alignContent: 'center', marginLeft: 'auto', marginRight: 'auto', marginTop: 'auto'}}>
      <Grid width={'75vw'} marginTop={10}>
        <Grid item xs={12} md={2}>
          <Drawer
            anchor="left"
            open={isDrawerOpen}
            onClose={() => setDrawerOpen(false)}
          >
            <div
              style={{
                width: '250px',
                padding: '16px',
                display: 'flex',
                flexDirection: 'column',
              }}
            >
              <Button
                startIcon={<MenuIcon />}
                onClick={() => setDrawerOpen(false)}
              >
                Close Menu
              </Button>
              <Divider />
              <List>
              {/* <ListItem button onClick={handleOpenAuthDialog}>
                  <ListItemIcon>
                    <AccountCircleIcon />
                  </ListItemIcon>
                  <ListItemText primary="Login" />
                </ListItem> */}
                <ListItem
                  button
                  selected={selectedMenu === 'mydrive'}
                  onClick={() => handleMenuClick('mydrive')}
                >
                  <ListItemIcon>
                    <FolderIcon />
                  </ListItemIcon>
                  <ListItemText primary="My Drive" />
                </ListItem>
                <ListItem
                  button
                  selected={selectedMenu === 'documents'}
                  onClick={() => handleMenuClick('documents')}
                >
                  <ListItemIcon>
                    <DescriptionIcon />
                  </ListItemIcon>
                  <ListItemText primary="Документы" />
                </ListItem>
                <ListItem
                  button
                  selected={selectedMenu === 'image'}
                  onClick={() => handleMenuClick('image')}
                >
                  <ListItemIcon>
                    <ImageIcon />
                  </ListItemIcon>
                  <ListItemText primary="Фото" />
                </ListItem>
                <ListItem
                  button
                  selected={selectedMenu === 'recent'}
                  onClick={() => handleMenuClick('recent')}
                >
                  <ListItemIcon>
                    <InsertDriveFileIcon />
                  </ListItemIcon>
                  <ListItemText primary="Другое" />
                </ListItem>
              </List>
              <Divider />
              <div align="center">
                <FileUploader userId={userId} onFileUpload={handleFileUpload} />
              </div>
            </div>
          </Drawer>
        </Grid>
        <Grid item xs={12} md={10}>
          <AppBar position="static" color="default">
            <Toolbar>
              <Grid item xs={12} sm={6} md={4}>
                <Typography variant="h6" color="inherit" marginLeft={1} marginTop={1}>
                    File Manager
                </Typography>
                <div>
                  <Button
                    startIcon={<MenuIcon />}
                    onClick={() => setDrawerOpen(true)}
                  >
                    Open Menu
                  </Button>
                </div>
              </Grid>
            </Toolbar>
          </AppBar>
          <Paper elevation={10} style={{ padding: '20px' }}>
          {!files.length ? <h1>К сожалению, пока ничего не найдено</h1>:
            <Grid container spacing={-2}>
                {files.map((file, index) => (
                    <FileCard key={index} file={file} selectedMenu={selectedMenu}/>
                ))}
            </Grid>
            }
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}

export default FileManager;
