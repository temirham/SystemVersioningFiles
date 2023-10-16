import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";
import { IP4, LoadingStatus, SuccessStatus } from "./pref";


async function fetchJSON(url, options) {
    let response = await fetch(url, options);
    if (!response.ok) {
        throw new Error(`status code ${response.status}`);
    }
    return response.json();
}

export const loadFiles = () => async (dispatch) => {
    try {
      const requestOptions = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
      },
    };
      const response = await axios.get(`${IP4}files_versioning_api/v1/files`, requestOptions);
      dispatch(setFile(response.data.data)); 
    } catch (error) {
    }
  };

// Замените Note на FileVersion
export const getUserFile = createAsyncThunk(
  'file/getUserFile',
  //async (userId) => {
  async () => {
    // const requestOptions = {
    //   headers: {
    //     'Content-Type': 'application/json',
    //     'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
    //   },
    // };
    // const response = await axios.get(`${IP4}file/${userId}`, requestOptions);
    const response = await axios.get(`https://650a3278f6553137159c7e12.mockapi.io/uploadFile`);
    return response.data.data
  }
);

// Замените Note на FileVersion
export const addFile = createAsyncThunk(
  'file/addFile',
  async (file) => {
    return await fetchJSON(
      `${IP4}`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json;charset=utf-8',
          'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
        },
        body: JSON.stringify({
          user: file.user,
          name: file.name,
          version: file.version,
        })
      }
    );
  }
);

export const uploadFile = createAsyncThunk(
    'file/uploadFile',
    async (formData) => {
      try {
        const response = await axios.post(`${IP4}/files_versioning_api/v1/files/add`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
          },
        });
        console.log('File uploaded successfully', response);
        return response.data.data
      } catch (error) {
        console.error('Error uploading file', error);
      }
    }
  );




// Замените Note на FileVersion
export const deleteFile = createAsyncThunk(
  'fileVersions/deleteFileVersion',
  async (file) => {
    return await fetchJSON(
      `${IP4}files_versioning_api/v1/files/delete/version`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json;charset=utf-8',
          'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
        },
        body: JSON.stringify({
          name: file.name,
          version: file.version
        })
      }
    );
  }
);

export const fileSlice = createSlice({
  name: "fileSlice",
  initialState: {
    files: [],
    fileStatus: '',
    currentFile: {
      fileName: '',
      version: 0,
      path: '',
      date: '',
    },
    deletingFile: {
      fileName: '',
      version: 0,
      path: '',
      date: '',
    },
    fileName: '',
  },
  reducers: {
    clearFile: (state, action) => {
      state.files = [];
      state.fileStatus = '';
      state.currentFile = {
        fileName: '',
        version: 0,
        path: '',
        date: '',
      };
      state.deletingFile = {
        fileName: '',
        version: 0,
        content: '',
        date: '',
      };
      state.fileName = '';
      localStorage.clear();
    },
    setFile: (state, action) => {
      state.files = action.payload;
    },
    setCurrentFile: (state, action) => {
      state.currentFile = action.payload;
    },
    setDeletingFile: (state, action) => {
      state.deletingFileVersion = action.payload;
    },
    setFileName: (state, action) => {
      state.fileName = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(getUserFile.pending, (state, action) => {
        state.fileStatus = LoadingStatus;
      })
      .addCase(getUserFile.fulfilled, (state, action) => {
        state.fileStatus = SuccessStatus;
        state.files = action.payload;
        state.currentFile = state.files[0];
        state.fileName = state.files[0].fileName;
        localStorage.setItem('file', JSON.stringify(state.files));
      })
      .addCase(getUserFile.rejected, (state, action) => {
        state.fileStatus = LoadingStatus;
        state.files = JSON.parse(localStorage.getItem('file'));
      })
      .addCase(addFile.pending, (state, action) => {
        state.fileStatus = LoadingStatus;
      })
      .addCase(addFile.fulfilled, (state, action) => {
        state.fileStatus = SuccessStatus;
      })
      .addCase(addFile.rejected, (state, action) => {
        state.fileStatus = LoadingStatus;
      })
      .addCase(deleteFile.pending, (state, action) => {
        state.fileStatus = LoadingStatus;
      })
      .addCase(deleteFile.fulfilled, (state, action) => {
        state.fileStatus = SuccessStatus;
      })
      .addCase(deleteFile.rejected, (state, action) => {
        state.fileStatus = LoadingStatus;
      });
  }
});

export const {
  clearFile,
  setFile,
  setCurrentFile,
  setDeletingFile,
  setOldFileName,
} = fileSlice.actions;

export default fileSlice.reducer;
