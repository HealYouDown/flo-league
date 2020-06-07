import React, { useState } from "react";
import { ContentWrapper } from "../Layout/LayoutStyles";
import { login } from "../../fetch";
import { loginUser } from "../../auth";
import strings from "../../localization/strings";

const Login = (props) => {
  document.title = strings.login;

  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")

  const loginRequest = (event) => {
    event.preventDefault();

    let res;
    login(username, password).then(fetchResponse => {
      res = fetchResponse;
      return fetchResponse.json();
    }).then(json => {
      if (!res.ok) {
        alert(json.msg);
      } else {
        loginUser(json.access_token);
        props.history.push("/")
      }
    });
  }

  return (
    <ContentWrapper>
      <form onSubmit={loginRequest}>
        <input
          value={username}
          onChange={e => setUsername(e.target.value)}
          placeholder={strings.username}
        />

        <input
          value={password}
          onChange={e => setPassword(e.target.value)}
          placeholder={strings.password}
        />

        <button type="submit">{strings.login}</button>
      </form>
    </ContentWrapper>
  )
}

export default Login;