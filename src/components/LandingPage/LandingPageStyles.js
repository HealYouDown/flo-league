import breakpoint from "../../breakpoint";
import { getImagePath } from "../../helpers";
import styled from "styled-components";

const Banner = styled.div`
  background-image: url(${getImagePath("banner_compressed.jpg")});
  background-size: cover;
  background-position-y: 40%;
  background-position-x: center;
  width: 100%;
  height: 350px;
  position: relative;
  border-bottom: 1px solid #cacaca;
`

const Grid = styled.div`
  display: grid;
  grid-column-gap: 40px;
`

const GridItem = styled.div`
  grid-row: ${props => props.rowS};
  grid-column: ${props => props.startS} / ${props => props.endS};
  ${breakpoint("lg")`
    grid-row: ${props => props.row};
    grid-column: ${props => props.start} / ${props => props.end};
  `}
`

export {
  Banner,
  Grid,
  GridItem,
}