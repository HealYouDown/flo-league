import React, { useState } from "react";
import { Link as RouterLink } from "react-router-dom";
import { getImagePath } from "../../helpers";
import { logoutUser, isLoggedIn, getIdentity } from "../../auth";
import {
  Nav,
  Main,
  Footer,
  LinksWrapper,
  Link,
  HeaderBrandLogo,
  NavbarExtension,
  LanguageSelect,
} from "./LayoutStyles";
import strings from "../../localization/strings";

const Layout = (props) => {
  const [loggedIn, setLoggedIn] = useState(isLoggedIn());
  const [selectedLanguage, setSelectedLanguage] = useState(
    localStorage.getItem("language") || "en"
  );

  strings.setLanguage(selectedLanguage);

  const logout = () => {
    logoutUser();
  }

  const onLanguageChange = (event) => {
    const newLanguage = event.target.value;
    localStorage.setItem("language", newLanguage);
    setSelectedLanguage(newLanguage);
    strings.setLanguage(newLanguage);
    window.location.reload();
  }

  window.addEventListener("storage", () => setLoggedIn(isLoggedIn()));

  return (
    <>
      {loggedIn && (
        <NavbarExtension>
          <LinksWrapper>
            <Link to="#" onClick={logout}>{getIdentity().username}</Link>
            <Link to="/create_matches/bergruen">{strings.createMatchesLink}</Link>
            <Link to="/players/add">{strings.addPlayerLink}</Link>
          </LinksWrapper>
        </NavbarExtension>
      )}
      <Nav>
        <RouterLink to="/">
          <HeaderBrandLogo src={getImagePath("logo_small.png")} />
        </RouterLink>
        <LinksWrapper>
          <Link to="/ranking/bergruen">{strings.rankingLink}</Link>
          <Link to="/active_matches/bergruen">{strings.matchesLink}</Link>
        </LinksWrapper>
      </Nav>

      <Main>{props.children}</Main>

      <Footer>
        <LinksWrapper>
          <Link to="/legal_notice">{strings.legalNoticeLink}</Link>
          <Link to="/privacy_policy">{strings.privacyPolicyLink}</Link>
          <LanguageSelect onChange={onLanguageChange} value={selectedLanguage}>
            <option value="en">English</option>
            <option value="de">Deutsch</option>
            <option value="it">Italiano</option>
            <option value="tr">Türk</option>
          </LanguageSelect>
        </LinksWrapper>
      </Footer>
    </>
  )
}

export default Layout;
