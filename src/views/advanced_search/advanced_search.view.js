import React, {useEffect} from "react";
import {Link, withRouter} from 'react-router-dom';
import {useFormik} from "formik";
import _ from 'lodash';
import {formikApiErrorsCatcher} from "../../utils/catcher";
import {CircularProgress, Box, Grid, IconButton, InputAdornment, TextField, Tooltip, Button, Typography} from "@material-ui/core";
import {SearchOutlined as SearchIcon, ArrowForwardIosOutlined as GoIcon} from "@material-ui/icons";
import LOGO from "../../images/Logo.png";
import { createTheme, ThemeProvider } from "@material-ui/core/styles";
import * as Yup from "yup";
import {useSnackbar} from "notistack";
import {TITLE} from "../../config";

const initialValues = {
    keyword: '',
    advanced: true,
};

const theme = createTheme({
    typography: {
      fontFamily: 'Beau Rivage',
    }
  });

const validationSchema = Yup.object({
    keyword: Yup.string("Enter a regular expression").required("Regex is required"),
    advanced: Yup.boolean("Enter is advanced").required("Advanced is required"),
});

const View = ({setTitle, fetchSearch, resetSearch, history}) => {
    const {enqueueSnackbar} = useSnackbar();
    useEffect(() => {
        setTitle(TITLE('Advanced Search'));
        resetSearch();
    }, [setTitle, resetSearch]);
    const myOnSubmit = () => {
        fetchSearch({...formik.values}).then(res => {
            formik.setSubmitting(false);
            if (!res || _.isEmpty(res) || (typeof res == "string")) {
                enqueueSnackbar(`Your regex search - ${formik.values.keyword} - did not match any books.`, {variant: 'info'});
            } else {
                history.push('/results');
            }
        }).catch((err) => {
            const errorMessage = formikApiErrorsCatcher(err, null, enqueueSnackbar);
            formik.setFieldError('keyword', errorMessage);
            formik.setSubmitting(false);
        });
    }
    const formik = useFormik({
        initialValues: initialValues,
        validationSchema: validationSchema,
        onSubmit: myOnSubmit,
    });

    return (
        <form noValidate>
            <Box mt={4}>
                <Grid display="flex"
                      container
                      spacing={24}
                      justify="center"
                      style={{ minHeight: '100vh', maxWidth: '100%' }}>
                    < Grid item xs={9}>
                        <ThemeProvider theme={theme}>
                            <Typography variant="h1" component="h1" align="center">
                                Gutenberg-Search
                            </Typography>
                        </ThemeProvider>
                    </Grid>
                <Grid
                    container
                    justify='center'
                    direction='column'
                    alignItems='center'
                >
                     <Grid item xs={9} style={{display: 'flex',  justifyContent:'center', alignItems:'center', height: '100vh'}}>
                        <img src={LOGO} alt='Gutenberg-Search' style={{
                            objectFit: 'scale-down',
                            scale: '0.5',
                        }}/>
                    </Grid>

                    <Grid item style={{width: '100%'}}>
                        <TextField
                            variant="outlined"
                            fullWidth
                            autoFocus
                            name="keyword"
                            placeholder="Search by RegEx ..."
                            helperText={""}
                            error={formik.touched.keyword && Boolean(formik.errors.keyword)}
                            onChange={formik.handleChange}
                            onBlur={formik.handleBlur}
                            value={formik.values.keyword}
                            InputProps={{
                                endAdornment: (
                                    <InputAdornment position="end">
                                        <Tooltip title='Search'>
                                            <span>
                                                <IconButton
                                                    color="primary"
                                                    onClick={formik.handleSubmit}
                                                    type="submit"
                                                    variant="contained"
                                                    disabled={!formik.isValid || formik.isSubmitting}
                                                >
                                                    {
                                                        formik.isSubmitting ? (
                                                            <CircularProgress size={24}/>
                                                        ) : (

                                                            <GoIcon/>
                                                        )
                                                    }
                                                </IconButton>
                                            </span>
                                        </Tooltip>
                                    </InputAdornment>
                                ),
                                startAdornment: (
                                    <InputAdornment position='start'>
                                        <SearchIcon color={"secondary"} fontSize="large"/>
                                    </InputAdornment>
                                ),
                            }}
                        />
                    </Grid>

                    <Grid item>
                        <Box mt={10}>
                            <Button
                                component={Link}
                                to={'/search'}
                                color='primary'
                                variant="contained"
                                size='large'
                            >
                                Search by Keyword
                            </Button>
                        </Box>
                    </Grid>
                </Grid>
                </Grid>
            </Box>
        </form>
    );
}

export default withRouter(View);