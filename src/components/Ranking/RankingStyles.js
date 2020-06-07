import styled from "styled-components";

const TableWrapper = styled.div`
  overflow-x: auto;
`

const Table = styled.table`
  width: 100%;
  border-collapse: collapse;

  th, td {
    padding: 10px 15px;
  }
`

const TableHeader = styled.th`
  text-align: ${props => props.align};
  white-space: nowrap;
`

const TableData = styled.td`
  text-align: ${props => props.align};
  white-space: nowrap;
`

const TableRow = styled.tr`
  background-color: ${props => props.even ? "white" : "#F8F8F8"};
`

export {
  TableWrapper,
  Table,
  TableHeader,
  TableData,
  TableRow,
}