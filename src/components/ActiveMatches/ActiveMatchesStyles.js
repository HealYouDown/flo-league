import styled from "styled-components";
import breakpoint from "../../breakpoint";
import { getImagePath } from "../../helpers";

const Line = styled.hr`
  border: none;
  border-bottom: 1px solid #cacaca;
  margin: 15px 0px;
  width: 100%;
  ${breakpoint("md")`
    width: 50%;
  `}
  ${breakpoint("lg")`
    width: 60%;
  `}
`

const VersusWrapper = styled.div`
  background-image: url(${getImagePath("swords.png")});
  background-repeat: no-repeat;
  background-position: center;
  background-size: 60px 60px;
  padding: 40px 50px;
  ${breakpoint("md")`
    padding: 40px 70px;
  `}
  ${breakpoint("lg")`
    padding: 40px 100px;
  `}
  ${breakpoint("xl")`
    padding: 40px 120px;
  `}
`

const VersusText = styled.span`
  color: #292f33;
  font-size: 20px;
  font-weight: 800;
`

const PlayerSub = styled.span`
  white-space: nowrap;
  font-size: 11px;
`

const EloGain = styled.span`
  color: green;
`


export {
  Line,
  VersusWrapper,
  VersusText,
  PlayerSub,
  EloGain,
}