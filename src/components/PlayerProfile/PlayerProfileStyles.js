import styled from "styled-components";
import breakpoint from "../../breakpoint";

const Grid = styled.div`
  display: grid;
  grid-column-gap: 40px;
  grid-row-gap: 40px;
  grid-template-columns: 100%;
  ${breakpoint("sm")`
    grid-template-columns: 30% 65%;
  `}
`

const PlayerInfoColumn = styled.div`
  grid-column: 1;
`

const PlayerInfoName = styled.span`
  font-size: 18px;
  letter-spacing: 1.5px;
`

const PlayerInfoTable = styled.table`
  width: 100%;
  border-collapse: collapse;
  margin-top: 5px;

  td {
    padding: 5px 10px;
  }
`

const MatchHistoryColumn = styled.div`
  grid-column: 1;
  ${breakpoint("sm")`
    grid-column: 2;
  `}
  display: flex;
  flex-flow: column;
  overflow-x: auto;
`

const MatchHistoryTable = styled.table`
  width: 100%;
  border-collapse: collapse;

  td, th {
    text-align: left;
    padding: 10px 15px;
  }
`

const ResultSpan = styled.span`
  color: ${props => props.color};
`

const TableRow = styled.tr`
  background-color: ${props => props.even ? "white" : "#F8F8F8"};
`

export {
  Grid,
  PlayerInfoColumn,
  PlayerInfoTable,
  PlayerInfoName,
  MatchHistoryColumn,
  ResultSpan,
  TableRow,
  MatchHistoryTable,
}