import React from "react";
import {Grid, Box, Typography, Link as UILink} from "@material-ui/core";
import LOGO from "../../images/Logo.png";
import {Link} from "react-router-dom";

export default class extends React.PureComponent {
    render() {
        return <Box mt={8}>
            <Grid
                container
                justify='center'
                alignItems='center'
                direction='column'
            >
                <Grid item xs={12} sm={11} md={10} lg={9} xl={8}>
                    <Box p={8}>
                        <Box p={2} mb={4}>
                            <Grid container justify='center'>
                                <Link to='/'>
                                    <img style={{
                                        height: 256,
                                        objectFit: 'contain',
                                    }} src={LOGO} alt="Gutenberg-Search"/>
                                </Link>
                            </Grid>
                        </Box>
                        <Typography variant='subtitle2' align='center' paragraph>Gutenberg-Search 2022</Typography>
                        <Typography variant='body1' align='left'>
                            Gutenberg-Search is a web application that allows you to search for books developped as a final Project for DAAR.
                        </Typography>
                        <Box my={2}>
                            <Typography variant='h6' align='left'>Authors</Typography>
                            <Box ml={2}>
                                <UILink
                                    variant="subtitle1"
                                    color="textPrimary"
                                    target="_blank"
                                    href='https://www.linkedin.com/in/habib-bouchenaki-963523222/'
                                    component='a'
                                >
                                    Habib BOUCHENAKI
                                </UILink>
                                <br/>
                                <UILink
                                    variant="subtitle1"
                                    color="textPrimary"
                                    target="_blank"
                                    href='https://www.linkedin.com/in/florent-meynier-447bba15a/'
                                    component='a'
                                >
                                    Florent MEYNIER
                                </UILink>
                                <br/>
                            </Box>
                            <br/>
                        </Box>
                    </Box>
                </Grid>
            </Grid>
        </Box>
    }
}