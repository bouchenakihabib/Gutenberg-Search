import {createTheme} from "@material-ui/core";
import {blueGrey} from "@material-ui/core/colors";
import theme from "../../theme";

export default createTheme({
    palette: {
        primary: {
            main: theme.COLOR_PRIMARY,
        },
        secondary: {
            main: blueGrey[500],
        },
        primaryText: {
            main: theme.COLOR_DEFAULT,
        }
    },
});