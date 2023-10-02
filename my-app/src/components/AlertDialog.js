import {useEffect, useState} from 'react';
import {
    Button,
    CircularProgress,
    Dialog,
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle, Grid
} from "@mui/material";
import {useDispatch, useSelector} from "react-redux";
import {closeAlert, openAlert} from "../store/UserSlice";
import {ErrorStatus, LoadingStatus, SuccessStatus} from "../store/pref";

export default function AlertDialog(message) {
  const dispatch = useDispatch();
  const {alertOpen} = useSelector((state) => state.alertOpen);
  const [path, setPath] = useState("/");


  useEffect(() => {
      const next_page = async() => {
          if (message.mode==="logging"){
              setPath("/notes")
          }
          if (message.mode==="registering"){
              setPath("/log")
          }
      }

      next_page()
  },[])
  const handleClose = async() => {
      await dispatch(closeAlert())
      message.type=""
  };

  return (
    <div>

      <Dialog
        open={alertOpen}
        onClose={handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">{message.title}</DialogTitle>
          {message.type === ErrorStatus &&
              <>
                  <DialogContent>
                      <DialogContentText id="alert-dialog-description">
                          {message.text}
                      </DialogContentText>
                  </DialogContent>
                  <DialogActions>
                  <Button
                  onClick={handleClose}
                  color="primary" autoFocus>
                  ок
                  </Button>
                  </DialogActions>
              </>
          }
          {message.type === LoadingStatus &&
              <>
                  <DialogContent>
                      <Grid
                            container
                            direction="column"
                            justifyContent="center"
                            alignItems="center"
                        >
                      <CircularProgress color="secondary" />
                      </Grid>
                  </DialogContent>
              </>
          }
          {message.type === SuccessStatus &&
                  <>
                      <DialogContent>
                          <DialogContentText id="alert-dialog-description">
                              {message.text}
                          </DialogContentText>
                      </DialogContent>
                      <DialogActions>
                          { message.mode==="logging" &&
                              <Button
                          onClick={handleClose} href={"/notes"}
                          color="primary" autoFocus>
                          ок
                          </Button>
                          }
                          { message.mode==="registering" &&
                              <Button
                          onClick={handleClose} href={"/login"}
                          color="primary" autoFocus>
                          ок
                          </Button>
                          }

                      </DialogActions>
                  </>
          }
      </Dialog>
    </div>
  );
}
