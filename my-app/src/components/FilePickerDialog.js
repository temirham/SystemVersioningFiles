import React, { useState } from 'react';
import { Button, Input, Paper, Typography } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

function FilePickerDialog({ onSelectFile, onClose }) {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleUpload = () => {
    if (selectedFile) {
      onSelectFile(selectedFile);
      onClose();
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    setSelectedFile(file);
    onSelectFile(file);
    onClose();
  };

  return (
    <Paper
      elevation={3}
      onDragOver={handleDragOver}
      onDrop={handleDrop}
      style={{
        padding: '20px',
        textAlign: 'center',
        cursor: 'pointer',
      }}
    >
      <Typography variant="h6">Drag and Drop to Upload</Typography>
      <Typography variant="body2">or</Typography>
      <Input type="file" onChange={handleFileChange} style={{ display: 'none' }} id="file-input" />
      <label htmlFor="file-input">
        <Button
          variant="contained"
          color="primary"
          component="span"
          startIcon={<CloudUploadIcon />}
        >
          Choose File
        </Button>
      </label>
    </Paper>
  );
}

export default FilePickerDialog;
