import styled from "styled-components";
import { Link } from "react-router-dom";

const ClassIcon = styled.img`
  border-radius: 50%;
  width: ${props => props.width}px;
  margin-right: ${props => props.marginRight}px;
  border: 4px solid rgba(202, 202, 202, 0.4);
`

const RouterLink = styled(Link)`
  text-decoration: none;
  color: unset;
`

const CenteredSpan = styled.span`
  display: block;
  text-align: center;
`

const H2 = styled.h2`
  color: #20123a;
  border-bottom: 1px solid #cacaca;
`

const Flex = styled.div`
  display: flex;
  flex-flow: ${props => props.flexFlow};
  justify-content: ${props => props.justifyContent};
  align-items: ${props => props.alignItems};
`

const Button = styled.button`
  transition: background-color 0.2s;
  transition: border-color 0.1s;
  background: white;
  color: black;
  border: 1px solid #cacaca;
  border-radius: 3px;
  cursor: pointer;
  width: ${props => props.width};
  margin: ${props => props.margin};
  padding: ${props => props.padding};
  font-size: ${props => props.fontSize};

  &:hover {
    background-color: ${props => props.backgroundColorOnHover};
    border-color: ${props => props.borderColorOnHover};
  }
`

const Text = styled.div`
  p, span, ul {
    color: ${props => props.textColor ? props.textColor : "#292f33"};
    text-align: justify;
  }

  ul {
    list-style: none;
    margin: 0px 0px;
    padding: 0px 0px;

    li:not(:first-child) {
      margin-top: 5px;
    }
  }
`

export {
  ClassIcon,
  RouterLink,
  CenteredSpan,
  H2,
  Flex,
  Button,
  Text,
}
