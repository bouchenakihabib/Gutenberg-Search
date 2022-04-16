import React from "react";
import {
    BrowserRouter as Router, 
    Switch,
} from "react-router-dom";
import Route from '../components/RouteWrapper';
import Book from '../views/book';
import About from '../views/about';
import AdvancedSearch from '../views/advanced_search';
import Search from '../views/search';
import Results from '../views/results';
import {Helmet} from 'react-helmet-async';
import Layout from '../components/Layout';


export default class extends React.PureComponent {
    render() {
        const {empty, title = "Gutenberg-Search"} = this.props;
        return (
            <>
                <Helmet>
                    <title>{title}</title>
                </Helmet>
                <Router>
                    {
                        !empty ? (
                                <Switch>
                                    <Route exact path="/book/:id" component={Book} layout={Layout}/>
                                    <Route path="/results" component={Results} layout={Layout}/>
                                    <Route path="/about" component={About} layout={Layout}/>
                                    <Route path="/advanced-search" component={AdvancedSearch} layout={Layout}/>
                                    <Route path="*" component={Search} layout={Layout}/>
                                </Switch>
                            ) :
                            (
                                <Switch>
                                    <Route exact path="/book/:id" component={Book} layout={Layout}/>
                                    <Route path="/about" component={About} layout={Layout}/>
                                    <Route path="/advanced-search" component={AdvancedSearch} layout={Layout}/>
                                    <Route path="*" component={Search} layout={Layout}/>
                                </Switch>
                            )
                    }
                </Router>
            </>
        );
    }
}