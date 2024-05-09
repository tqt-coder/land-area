import styled from "styled-components";

const Select = styled.select`
  width: 100px;
  & + select {
    margin-left: 10px;
  }
`;

export { Select };
