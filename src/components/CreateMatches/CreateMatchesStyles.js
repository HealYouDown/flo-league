import styled from "styled-components";

const Grid = styled.div`
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-column-gap: 50px;
`

const SearchPlayerColumn = styled.div`
  grid-column: 1 / 2;
  grid-row: 1 / 2;
`

const AddedPlayerColumn = styled.div`
  grid-column: 2 / 3;
  grid-row: 1 / 3;
`

const ChatlogPlayerColumn = styled.div`
  grid-column: 1 / 2;
  grid-row: 2 / 3;
`

const ChatlogWrapper = styled.div`
  display: flex;
  flex-flow: column;

  * {
    flex-grow: 1;
  }
`

const AddedPlayerList = styled.div`
  display: flex;
  flex-flow: column;
  > div:not(:first-child) {
    border-top: 1px solid #cacaca;
  }
`

const SearchResults = styled.div`
  display: flex;
  flex-flow: column;
  max-height: 200px;
  overflow-y: auto;

  > div:not(:first-child) {
    border-top: 1px solid #cacaca;
  }
`

const PlayerWrapper = styled.div`
  display: flex;
  align-items: center;
  padding: 5px 0px;

  &:hover {
    background-color: #F8F8F8;
    cursor: pointer;
  }
`

const SearchInput = styled.input`
  width: 100%;
  font-size: 18px;
  border-radius: 5px;
  border: 1px solid #cacaca;  
  padding: 5px 10px;
`

const KeywordInput = styled.input`
  border-radius: 5px;
  border: 1px solid #cacaca;  
  padding: 5px 10px;
`

const SearchInputWrapper = styled.div`
  display: flex;
  margin-bottom: 5px;
  > input {
    flex-grow: 1;
  }
`

const ChatlogTextArea = styled.textarea`
  height: 400px;
  border-radius: 5px;
  border: 1px solid #cacaca;
  margin-top: 4px;
`

export {
  Grid,
  SearchPlayerColumn,
  AddedPlayerColumn,
  ChatlogPlayerColumn,
  ChatlogWrapper,
  AddedPlayerList,
  SearchResults,
  PlayerWrapper,
  SearchInput,
  KeywordInput,
  SearchInputWrapper,
  ChatlogTextArea,
}