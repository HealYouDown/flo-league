import styled from "styled-components";
import { Link as RouterLink } from "react-router-dom";
import breakpoint from "../../breakpoint";

const Nav = styled.nav`
  background: white;
  padding: 8px 0px;
  display: flex;
  justify-content: space-around;
  border-bottom: 1px solid #cacaca;
`;

const LinksWrapper = styled.div`
  display: flex;
  justify-content: space-around;
  align-items: center;
`

const Link = styled(RouterLink)`
  margin: 5px 5px;
  ${breakpoint("sm")`
    margin: 5px 30px;
  `}
  color: ${props => props.isactive ? "green" : "black"};
  text-decoration: none;
  letter-spacing: 1.2px;

  &:hover {
    cursor: pointer;
    text-decoration: underline;
  }
`

const HeaderBrandLogo = styled.img`
  height: 50px;
  width: auto;
`

const Main = styled.main``;

const ContentWrapper = styled.div`
  padding: 0px 20px;
  ${breakpoint("lg")`
    padding: 0px 125px;
  `}
  ${breakpoint("xl")`
    padding: 0px 250px;
  `}
  margin: 20px 0px;
`

const Footer = styled.footer`
  padding: 8px 0px;
  border-top: 1px solid #cacaca;
`;

const NavbarExtension = styled.div`
  display: flex;
  flex-flow: row;
  justify-content: space-around;
  align-items: center;
  padding: 5px 0px;
  border-bottom: 1px solid #cacaca;
`

const LanguageSelect = styled.select`
  border: 1px solid #cacaca;
  border-radius: 3px;
  color: black;
  padding: 5px 10px;
`

export {
  Nav,
  Main,
  Footer,
  LinksWrapper,
  Link,
  HeaderBrandLogo,
  ContentWrapper,
  NavbarExtension,
  LanguageSelect,
}