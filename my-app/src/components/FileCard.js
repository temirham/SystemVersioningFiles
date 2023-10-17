import React, { useState } from 'react';
import { useSelector } from 'react-redux';
import { Typography, Menu, MenuItem, Dialog, DialogTitle, DialogContent, List, ListItem, ListItemText } from '@mui/material';
import { Icon } from '@iconify/react';
import fileIcon from '@iconify-icons/fa-regular/file';
import fileImage from '@iconify-icons/fa-solid/file-image';
import filePdf from '@iconify-icons/fa-regular/file-pdf';
import fileWord from '@iconify-icons/fa-regular/file-word';
import fileExcl from '@iconify-icons/fa-regular/file-excel';
import filePpt from '@iconify-icons/fa-regular/file-powerpoint';
import { deleteFile, loadFiles } from '../store/fileSlice.js';
import { useDispatch } from "react-redux";
import axios from 'axios';

function getFileIcon(extension) {
  switch (extension.toLowerCase()) {
    case 'jpg':
      return <Icon icon={fileImage} />;
    case 'docx':
      return <Icon icon={fileWord} />;
    case 'xlsx':
      return <Icon icon={fileExcl} />;
    case 'doc':
      return <Icon icon={fileWord} />;
    case 'word':
      return <Icon icon={fileWord} />;
    case 'pptx':
      return <Icon icon={filePpt} />;
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

function FileCard({ file, selectedMenu }) {
  const [contextMenuAnchor, setContextMenuAnchor] = useState(null);
  const [contextMenuAnchor1, setContextMenuAnchor1] = useState(null);
  const [selectedVersionFile, setSelectedVersionFile] = useState(null);
  const dispatch = useDispatch();
  const { files } = useSelector((state) => state.files);
  const [isVersionsDialogOpen, setVersionsDialogOpen] = useState(false);

  const openVersionsDialog = () => {
    handleCloseContextMenu();
    setVersionsDialogOpen(true);
  };

  const closeVersionsDialog = () => {
    setVersionsDialogOpen(false);
  };

  const handleContextMenu = (event) => {
    event.preventDefault();
    setContextMenuAnchor(event.currentTarget);
  };

  const handleContextMenu1 = (event, versionFile) => {
    event.preventDefault();
    setContextMenuAnchor1(event.currentTarget);
    setSelectedVersionFile(versionFile);
  };

  const handleCloseContextMenu = () => {
    setContextMenuAnchor(null);
  };

  const handleCloseContextMenu1 = () => {
    setContextMenuAnchor1(null);
  };

  const handleDeleteVersion = (versionFile) => {
    dispatch(deleteFile(versionFile));
    dispatch(loadFiles());
    dispatch(loadFiles());
    handleCloseContextMenu1();
  };

  const handleDeleteFile = () => {
    const allVersionsToDelete = [file, ...files.filter((f) => f.name === file.name)];
    allVersionsToDelete.forEach((versionFile) => {
      dispatch(deleteFile(versionFile)).then(() => 
        {dispatch(loadFiles())}
    );
    });
    handleCloseContextMenu();
  };

  const handleDownloadFile = async (selectedFile) => {
    try {
      const requestData = {
        name: selectedFile.name,
        version: selectedFile.version
      };
      const response = await axios.post('http://127.0.0.1:8000/files_versioning_api/v1/files/download', requestData, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
        },
        responseType: 'arraybuffer', 
      });
  
      const blob = new Blob([response.data], { type: response.headers['content-type'] });
  
      const downloadUrl = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.setAttribute('download', selectedFile.name);
      document.body.appendChild(link);
      link.click();
      link.remove(); 
    } catch (error) {
      console.error('Ошибка загрузки файла:', error);
    }
    handleCloseContextMenu();
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
        return true;
    }
  };

  if (!file || !isFileTypeMatch(file, selectedMenu)) {
    return null;
  }

  return (
    <div style={{ marginLeft: '15px', marginRight: '15px', width: '6em' }}
    >
      <div
        style={{ fontSize: '60px', cursor: 'pointer' }}
        onContextMenu={handleContextMenu}
      >
        {getFileIcon(file.name.split('.').pop())}
      </div>
      <div >
        <Typography variant="subtitle3" style={{ fontSize: '13px' }}>{file.name}</Typography>
        <Typography variant="subtitle1">version: {file.version}</Typography>
      </div>
      <Menu
        anchorEl={contextMenuAnchor}
        open={Boolean(contextMenuAnchor)}
        onClose={handleCloseContextMenu}
      >
        <MenuItem onClick={handleDeleteFile}>Удалить</MenuItem>
        <MenuItem onClick={() => handleDownloadFile(file)}>Скачать</MenuItem>
        <MenuItem onClick={openVersionsDialog}>Показать все версии файла</MenuItem>
      </Menu>
      <Dialog open={isVersionsDialogOpen} onClose={closeVersionsDialog}>
        <DialogTitle>Версии файла: {file.name}</DialogTitle>
        <DialogContent>
          <List>
            {files
              .filter((f) => f.name === file.name)
              .map((versionFile, index) => (
                <ListItem key={index}>
                  <ListItemText
                    style={{ cursor: 'pointer' }}
                    onContextMenu={(event) => handleContextMenu1(event, versionFile)}
                    primary={`Версия ${versionFile.version}`}
                  />
                  <Menu
                    anchorEl={contextMenuAnchor1}
                    open={Boolean(contextMenuAnchor1) && versionFile === selectedVersionFile}
                    onClose={handleCloseContextMenu1}
                  >
                    <MenuItem onClick={() => handleDeleteVersion(versionFile)}>Удалить</MenuItem>
                    <MenuItem onClick={() => handleDownloadFile(versionFile)}>Скачать</MenuItem>
                  </Menu>
                </ListItem>
              ))}
          </List>
        </DialogContent>
      </Dialog>
    </div>
  );
}

export default FileCard;