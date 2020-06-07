import React from "react";
import {
  BrowserRouter as Router,
  Route,
  Switch,
} from "react-router-dom";
import { createGlobalStyle } from "styled-components";
import Layout from "./components/Layout/Layout";
import Ranking from "./components/Ranking/Ranking";
import LandingPage from "./components/LandingPage/LandingPage";
import ActiveMatches from "./components/ActiveMatches/ActiveMatches";
import PlayerProfile from "./components/PlayerProfile/PlayerProfile";
import Login from "./components/Login/Login";
import CreateMatches from "./components/CreateMatches/CreateMatches";
import PrivacyPolicy from "./components/FooterPages/PrivacyPolicy";
import LegalNotice from "./components/FooterPages/LegalNotice";
import PlayerEdit from "./components/PlayerEdit/PlayerEdit";
import PlayerAdd from "./components/PlayerEdit/AddPlayer";

const GlobalStyle = createGlobalStyle`
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

body {
  overflow-y: scroll;
}

#root {
  display: flex;
  flex-flow: column;
  height: 100% !important;
}

main {
  flex-grow: 1;
}
`

const App = () => {
  return (
    <Router>
      <Layout>
        <Switch>

          <Route exact path="/" component={LandingPage} />
          <Route path="/ranking/:server(bergruen|luxplena)" component={Ranking} />

          <Route path="/active_matches/:server(bergruen|luxplena)" component={ActiveMatches} />
          
          <Route path="/create_matches/:server(bergruen|luxplena)" component={CreateMatches} />

          <Route exact path="/players/:server(bergruen|luxplena)/:name" component={PlayerProfile} />
          <Route exact path="/players/:server(bergruen|luxplena)/:name/edit" component={PlayerEdit} />
          <Route exact path="/players/add" component={PlayerAdd} />

          <Route path="/login" component={Login} />

          <Route path="/privacy_policy" component={PrivacyPolicy} />
          <Route path="/legal_notice" component={LegalNotice} />

        </Switch>
      </Layout>
      <GlobalStyle />
    </Router>
  )
}

export default App;