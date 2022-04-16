import {makeStyles} from '@material-ui/core/styles';

export default makeStyles((theme) => ({
    root: {
        width: theme.spacing(48),
    },
    media: {
        objectFit: 'cover',
        objectPosition: 'top',
        height: theme.spacing(32),
    },
}));