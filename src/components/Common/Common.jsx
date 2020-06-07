import React from "react";
import { NavbarExtension as NavbarExtensionStyle, Link } from "../Layout/LayoutStyles";
import { CenteredSpan } from "./CommonStyles";
import strings from "../../localization/strings";

const NavbarExtension = ({currentServer, url}) => {
  return (
    <NavbarExtensionStyle>
      <Link
        isactive={(currentServer === "bergruen") ? true : false}
        to={`/${url}/bergruen`}
      >
        Bergruen
      </Link>
      <Link
        isactive={(currentServer === "luxplena") ? true : false}
        to={`/${url}/luxplena`}
      >
        LuxPlena
      </Link>
    </NavbarExtensionStyle>
  )
}

const FetchStateMessage = ({loading, error, children}) => {
  if (loading) {
    return <CenteredSpan>{strings.loadingMessage}</CenteredSpan>
  } else if (error) {
    return <CenteredSpan>{strings.errorMessage}</CenteredSpan>
  } else {
    return children;
  }
}

export {
  NavbarExtension,
  FetchStateMessage,
}