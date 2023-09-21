import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { Button, Avatar, Card, CardContent, Typography, CardActions} from '@mui/material';
import { uploadFile } from '/Users/temirhanmamaev/Documents/test_front/my-app/src/store/fileSlice.js';
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

function FileCard({ file, selectedMenu}) {
  const [selectedFile, setSelectedFile] = useState(null);
  const dispatch = useDispatch();
  const userId = 2;

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = () => {
    if (selectedFile) {
      dispatch(uploadFile({ file: selectedFile, userId }));
    }
  };
  const isFileTypeMatch = (file, fileType) => {
    const fileExtension = file.name.split('.').pop().toLowerCase();
    switch (fileType) {
      case 'documents':
        return ['pdf', 'word', 'doc', 'docx'].includes(fileExtension);
      case 'image':
        return ['jpg', 'jpeg', 'png', 'gif'].includes(fileExtension);
      case 'recent':
        return !['pdf', 'word', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'gif'].includes(fileExtension);
      default:
        return true; // Показываем все остальные файлы для 'recent' и 'mydrive'
    }
  };

  // Проверяем, соответствует ли файл выбору пользователя
  if (!isFileTypeMatch(file, selectedMenu)) {
    return null; // Не отображаем файлы, которые не соответствуют выбору
  }

  return (
    <Card variant="outlined" style={{ marginLeft: '10px', marginBottom: '10px'}}>
        <CardContent>
            <Avatar>{getFileIcon(file.name.split('.').pop())}</Avatar>
            <Typography variant="subtitle1">{file.name}</Typography>
        </CardContent>
        <CardActions>
            <Button
                variant="contained"
                color="secondary"
                startIcon={<DeleteIcon />}
            >
                Delete
            </Button>
            <Button variant="contained" color="primary" onClick={handleUpload}>
                Download
            </Button>
        </CardActions>
    </Card>
  );
}

export default FileCard;
