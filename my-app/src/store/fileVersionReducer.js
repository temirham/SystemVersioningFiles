import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  fileVersions: [], // Массив версий файлов
};

const fileVersionSlice = createSlice({
  name: 'fileVersion',
  initialState,
  reducers: {
    addFileVersion: (state, action) => {
      // Добавление новой версии файла
      state.fileVersions.push(action.payload);
    },
    deleteFileVersion: (state, action) => {
      // Удаление версии файла по индексу или идентификатору
      const index = state.fileVersions.findIndex(
        (version) => version.id === action.payload
      );
      if (index !== -1) {
        state.fileVersions.splice(index, 1);
      }
    },
  },
});

export const { addFileVersion, deleteFileVersion } = fileVersionSlice.actions;
export default fileVersionSlice.reducer;
