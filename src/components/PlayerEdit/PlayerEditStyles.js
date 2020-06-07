import styled from "styled-components";

const InputGroup = styled.div`
  display: flex;
  flex-flow: row;
  padding: 15px 20px;

  > input, select {
    flex-grow: 1;
  }

  > label {
    margin-right: 20px;
  }
`

const TextInput = styled.input`
  border: 1px solid #cacaca;
  border-radius: 4px;
  padding: 5px 10px;
`

const Select = styled.select`
  border: 1px solid #cacaca;
  border-radius: 4px;
  padding: 5px 10px;
`

export {
  InputGroup,
  TextInput,
  Select
}