import React, { useState } from 'react';
import { Button, Dialog, DialogActions, DialogContent, DialogTitle, Input, Paper, Typography } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile'; // Импортируем иконку файла

import { addFile, setCurrentFile, setFile} from '/Users/temirhanmamaev/Documents/test_front/my-app/src/store/fileSlice.js';

import {useDispatch, useSelector} from "react-redux";

function FileUploader({ onFileUpload }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isDialogOpen, setDialogOpen] = useState(false);
  const dispatch = useDispatch();
//   const {userId} = useSelector((state) => state.userId);
  const userId = 3;
  

  const openDialog = () => {
    setDialogOpen(true);
  };

  const closeDialog = () => {
    setDialogOpen(false);
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setSelectedFile(file);
  };

  const handleUpload = () => {
    if (selectedFile) {
        // dispatch(setCurrentFile({ 
        //     file: selectedFile.name, 
        //     version: 0,
        //     path: selectedFile.name,
        //     date: selectedFile.lastModified, 
        // }));
        dispatch(addFile(selectedFile))
        closeDialog();
      }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    setSelectedFile(file);
  };

  return (
    <div>
      <Button startIcon={<CloudUploadIcon />} variant="contained" color="primary" onClick={openDialog}>
        Выгрузить файл
      </Button>
      <Dialog open={isDialogOpen} onClose={closeDialog} maxWidth="md">
        <DialogTitle>Select a File</DialogTitle>
        <DialogContent>
          <Paper
            elevation={3}
            onDragOver={handleDragOver}
            onDrop={handleDrop}
            style={{
              padding: '40px',
              textAlign: 'center',
              cursor: 'pointer',
              minWidth: '500px',
              minHeight: '300px' // Увеличиваем минимальную ширину
            }}
          >
            {selectedFile ? (
              <div>
                <InsertDriveFileIcon
                  style={{
                    fontSize: '72px', // Устанавливаем размер иконки
                    color: 'gray', // Устанавливаем серый цвет для иконки
                    marginBottom: '20px', // Отступ снизу от иконки
                  }}
                />
                <Typography variant="h6">Выберите файл:</Typography>
                <Typography variant="subtitle1">{selectedFile.name}</Typography>
              </div>
            ) : (
              <div>
                <Typography variant="h6">Перетащите файл сюда</Typography>
                <Typography variant="h6">или</Typography>
                <Input type="file" onChange={handleFileChange} style={{ display: 'none' }} id="file-input" />
                <label htmlFor="file-input">
                  <Button
                    variant="contained"
                    color="primary"
                    component="span"
                    startIcon={<CloudUploadIcon />}
                    
                  >
                    Выбрать из проводника
                  </Button>
                </label>
              </div>
            )}
          </Paper>
        </DialogContent>
        <DialogActions>
          <Button onClick={closeDialog} color="primary">
            Close
          </Button>
          {selectedFile && (
            <Button onClick={handleUpload} color="primary">
              Upload
            </Button>
          )}
        </DialogActions>
      </Dialog>
    </div>
  );
}

export default FileUploader;
