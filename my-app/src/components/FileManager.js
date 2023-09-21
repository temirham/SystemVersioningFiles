import React, { useState, useEffect} from 'react';
import FileUploader from './FileUploader';
// import AuthDialog from './AuthDialog';
// import { Icon } from '@iconify/react';
// import fileIcon from '@iconify-icons/fa-regular/file';
// import fileImage from '@iconify-icons/fa-solid/file-image';
// import filePdf from '@iconify-icons/fa-regular/file-pdf';
// import fileWord from '@iconify-icons/fa-regular/file-word';
// import fileExcl from '@iconify-icons/fa-regular/file-excel';
// import filePpt from '@iconify-icons/fa-regular/file-powerpoint';
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
import { addFile, getUserFile } from '../store/fileSlice';
import { GetFiles } from '../Hooks/GetFiles';

// function getFileIcon(extension) {
//     switch (extension.toLowerCase()) {
//       case 'jpg':
//         return <Icon icon={fileImage} />;
//       case 'docx':
//         return <Icon icon={fileWord}/>;
//       case 'xlsx':
//         return <Icon icon={fileExcl}/>;
//       case 'doc':
//         return <Icon icon={fileWord}/>;
//       case 'word':
//         return <Icon icon={fileWord}/>;
//       case 'pptx':
//         return <Icon icon={filePpt}/>;
//       case 'jpeg':
//         return <Icon icon={fileImage} />;
//       case 'png':
//         return <Icon icon={fileImage} />;
//       case 'gif':
//         return <Icon icon={fileImage} />;
//       case 'pdf':
//         return <Icon icon={filePdf} />;
//       default:
//         return <Icon icon={fileIcon} />;
//     }
//   }
  

function FileManager() {
//   const [files, setFiles] = useState([]);
//   const [folders, setFolders] = useState([]);
//   const [newFolderName, setNewFolderName] = useState('');
// //   const [isAddingFolder, setIsAddingFolder] = useState(false);
  getUserFile(3)
  const [isDrawerOpen, setDrawerOpen] = useState(false);
  const [selectedMenu, setSelectedMenu] = useState('mydrive'); // Начальное значение выбора

  const handleMenuClick = (menu) => {
    setSelectedMenu(menu);
  };
  const dispatch = useDispatch();
  GetFiles()
  const {userId} = useSelector((state) => state.userId);
  const {username} = useSelector((state) => state.username);
  const {files} = useSelector((state) => state.files); // Замените на ваш собственный селектор для списка файлов
  useEffect(() => {
    const fetchData = async () => {
        await dispatch(refreshUser())
            .then(async ()=>{
                await dispatch(getUser())
                .then(async()=>{
                    await dispatch(getUserFile())
                })
                
            })
    }
    fetchData()
  }, [])
  const handleFileUpload = (selectedFile) => {
    if (selectedFile) {
        dispatch(uploadFile({ file: selectedFile, userId }));
      }
  };

//   const handleAdd=async ()=>{
//     let updatedCurrentNote={title:`new_note`, content:'', date:'', user:username}

//     await dispatch(refreshUser())
//         .then(async()=>{
//             await dispatch(addFileVersion(updatedCurrentNote))
//                 .then(async ()=>{
//                     await dispatch(getUserFileVersions(userId))
//                 })
//             await dispatch(getUserFileVersions(userId))
//                 .then((res)=>{console.log(res)})
//         })

//   }

//   const handleDeleteFile = (fileToDelete) => {
//     const updatedFiles = files.filter((file) => file !== fileToDelete);
//     setFiles(updatedFiles);
//   };

//   const handleCreateFolder = () => {
//     if (newFolderName.trim() !== '') {
//       setFolders([...folders, newFolderName]);
//       setNewFolderName('');
//       setIsAddingFolder(false);
//     }
//   };

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
                <FileUploader onFileUpload={handleFileUpload} />
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
