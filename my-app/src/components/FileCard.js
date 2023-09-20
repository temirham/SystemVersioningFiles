import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Button, Avatar, Card, CardContent, Typography, CardActions} from '@mui/material';
import { uploadFile } from '/Users/temirhanmamaev/Documents/test_front/my-app/src/store/fileSlice.js'; // Импортируйте действие

import { Icon } from '@iconify/react';
import DeleteIcon from '@mui/icons-material/Menu';
import fileIcon from '@iconify-icons/fa-regular/file';
import fileImage from '@iconify-icons/fa-solid/file-image';
import filePdf from '@iconify-icons/fa-regular/file-pdf';
import fileWord from '@iconify-icons/fa-regular/file-word';
import fileExcl from '@iconify-icons/fa-regular/file-excel';
import filePpt from '@iconify-icons/fa-regular/file-powerpoint';


function getFileIcon(extension) {
    switch (extension.toLowerCase()) {
      case 'jpg':
        return <Icon icon={fileImage} />;
      case 'docx':
        return <Icon icon={fileWord}/>;
      case 'xlsx':
        return <Icon icon={fileExcl}/>;
      case 'doc':
        return <Icon icon={fileWord}/>;
      case 'word':
        return <Icon icon={fileWord}/>;
      case 'pptx':
        return <Icon icon={filePpt}/>;
      case 'jpeg':
        return <Icon icon={fileImage} />;
      case 'png':
        return <Icon icon={fileImage} />;
      case 'gif':
        return <Icon icon={fileImage} />;
      case 'pdf':
        return <Icon icon={filePdf} />;
      default:
        return <Icon icon={fileIcon} />;
    }
  }

function FileCard({ file }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const dispatch = useDispatch();
  const files = useSelector((state) => state.fileVersions.files);
//   const userId = useSelector((state) => state.user.userId);
  const userId = 2; // Предположим, что у вас есть редюсер для пользователей с userId

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = () => {
    if (selectedFile) {
      dispatch(uploadFile({ file: selectedFile, userId }));
    }
  };
  const handleDeleteFile = (fileToDelete) => {
      const updatedFiles = files.filter((file) => file !== fileToDelete);
    //   setFiles(updatedFiles);
      if (updatedFiles) {
        dispatch(uploadFile({ file: updatedFiles, userId }));
      }
  };

  return (
    <Card variant="outlined">
        <CardContent>
            <Avatar>{getFileIcon(file.name.split('.').pop())}</Avatar>
            <Typography variant="subtitle1">{file.name}</Typography>
        </CardContent>
        <CardActions>
            <Button
                variant="contained"
                color="secondary"
                startIcon={<DeleteIcon />}
                onClick={() => handleDeleteFile(file)}
            >
                Delete
            </Button>
            <Button variant="contained" color="primary" onClick={handleUpload}>
                Upload File
            </Button>
        </CardActions>
    </Card>
  );
}

export default FileCard;
