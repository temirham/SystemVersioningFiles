import React, { useState } from 'react';
import FileUploader from './FileUploader';
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
import useDataFetching from '../Hooks/useDataFetching';
import useDataUpload from '../Hooks/useDataUpload';
 
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
// //   const [files, setFiles] = useState([]);
// //   const [folders, setFolders] = useState([]);
// //   const [newFolderName, setNewFolderName] = useState('');
// // //   const [isAddingFolder, setIsAddingFolder] = useState(false);
//   getUserFile(3)
//   const [isDrawerOpen, setDrawerOpen] = useState(false);
//   const dispatch = useDispatch();
//   const {userId} = useSelector((state) => state.userId);
//   const {username} = useSelector((state) => state.username);
//   const {files} = useSelector((state) => state.files); // Замените на ваш собственный селектор для списка файлов

//   const handleFileUpload = (selectedFile) => {
//     if (selectedFile) {
//         dispatch(uploadFile({ file: selectedFile, userId }));
//       }
//   };

// //   const handleAdd=async ()=>{
// //     let updatedCurrentNote={title:`new_note`, content:'', date:'', user:username}

// //     await dispatch(refreshUser())
// //         .then(async()=>{
// //             await dispatch(addFileVersion(updatedCurrentNote))
// //                 .then(async ()=>{
// //                     await dispatch(getUserFileVersions(userId))
// //                 })
// //             await dispatch(getUserFileVersions(userId))
// //                 .then((res)=>{console.log(res)})
// //         })

// //   }

// //   const handleDeleteFile = (fileToDelete) => {
// //     const updatedFiles = files.filter((file) => file !== fileToDelete);
// //     setFiles(updatedFiles);
// //   };

// //   const handleCreateFolder = () => {
// //     if (newFolderName.trim() !== '') {
// //       setFolders([...folders, newFolderName]);
// //       setNewFolderName('');
// //       setIsAddingFolder(false);
// //     }
// //   };

//   return (
//     <Container >
//       <Grid container spacing={3} width={'75vw'} marginTop={10}>
//         <Grid item xs={12} md={2}>
//           <Drawer
//             anchor="left"
//             open={isDrawerOpen}
//             onClose={() => setDrawerOpen(false)}
//           >
//             <div
//               style={{
//                 width: '250px',
//                 padding: '16px',
//                 display: 'flex',
//                 flexDirection: 'column',
//               }}
//             >
//               <Button
//                 startIcon={<MenuIcon />}
//                 onClick={() => setDrawerOpen(false)}
//               >
//                 Close Menu
//               </Button>
//               <Divider />
//               <List>
//                 <ListItem button>
//                   <ListItemIcon>
//                     <FolderIcon />
//                   </ListItemIcon>
//                   <ListItemText primary="My Drive" />
//                 </ListItem>
//                 <ListItem button>
//                   <ListItemIcon>
//                     <InsertDriveFileIcon />
//                   </ListItemIcon>
//                   <ListItemText primary="Recent" />
//                 </ListItem>
//                 <ListItem button>
//                   <ListItemIcon>
//                     <DescriptionIcon />
//                   </ListItemIcon>
//                   <ListItemText primary="Documents" />
//                 </ListItem>
//                 <ListItem button>
//                   <ListItemIcon>
//                     <ImageIcon />
//                   </ListItemIcon>
//                   <ListItemText primary="Photos" />
//                 </ListItem>
//               </List>
//               <Divider />
//               <div align="center">
//                 <FileUploader onFileUpload={handleFileUpload} />
//               </div>
              
//             </div>
//           </Drawer>
//         </Grid>
//         <Grid item xs={12} md={10}>
//           <AppBar position="static" color="default">
//             <Toolbar>
//               <Grid item xs={12} sm={6} md={4}>
//                 <Typography variant="h6" color="inherit" marginLeft={1} marginTop={1}>
//                     File Manager
//                 </Typography>
//                 <div>
//                   <Button
//                     startIcon={<MenuIcon />}
//                     onClick={() => setDrawerOpen(true)}
//                   >
//                     Open Menu
//                   </Button>
//                 </div>
//               </Grid>
//             </Toolbar>
//           </AppBar>
//           <Paper elevation={4} style={{ padding: '16px' }}>
//           {!files.length ? <h1>К сожалению, пока ничего не найдено</h1>:
//             <Grid container spacing={2}>
//               {/* {files.map((file, index) => (
//                 <Grid item xs={10} sm={6} md={4} key={index}>
//                   <Card variant="outlined">
//                     <CardContent>
//                       <Avatar>{getFileIcon(file.name.split('.').pop())}</Avatar>
//                       <Typography variant="subtitle1">{file.name}</Typography>
//                     </CardContent>
//                     <CardActions>
//                       <Button
//                         variant="contained"
//                         color="secondary"
//                         startIcon={<DeleteIcon />}
//                         onClick={() => handleDeleteFile(file)}
//                       >
//                         Delete
//                       </Button>
//                     </CardActions>
//                   </Card>
//                 </Grid>
//               ))} */}
//                 {files.map((file, index) => (
//                     <FileCard key={index} file={file} />
//                 ))}
//             </Grid>
//             }
//           </Paper>
//         </Grid>
//       </Grid>
//     </Container>
//   );
const apiUrl = 'https://650a3278f6553137159c7e12.mockapi.io/uploadFile'; // Замените на реальный URL API
//   const { data, isLoading, error } = useDataFetching(apiUrl);

//   if (isLoading) {
//     return <div>Загрузка данных...</div>;
//   }

//   if (error) {
//     return <div>Произошла ошибка: {error.message}</div>;
//   }

//   return (
//     <div>
//       <h1>Данные с сервера:</h1>
//       <pre>{JSON.stringify(data, null, 2)}</pre>
//     </div>
//   );
  const { isLoading, error, responseData, uploadData } = useDataUpload(apiUrl);
  const [dataToSend, setDataToSend] = useState({ key: 'value' }); // Замените на данные, которые вы хотите отправить

  const handleUploadClick = () => {
    uploadData(dataToSend);
  };

  if (isLoading) {
    return <div>Отправка данных...</div>;
  }

  if (error) {
    return <div>Произошла ошибка: {error.message}</div>;
  }

  if (responseData) {
    return (
      <div>
        <h1>Данные успешно отправлены:</h1>
        <pre>{JSON.stringify(responseData, null, 2)}</pre>
      </div>
    );
  }

  return (
    <div>
      <h1>Отправка данных на сервер</h1>
      <button onClick={handleUploadClick}>Отправить данные</button>
    </div>
  );
}

export default FileManager;
