import React, { useState } from "react";
import { addPlayer } from "../../fetch";
import { ContentWrapper } from "../Layout/LayoutStyles";
import { Button } from "../Common/CommonStyles";
import {
  InputGroup,
  TextInput,
  Select
} from "./PlayerEditStyles";
import strings from "../../localization/strings";

const PlayerAdd = (props) => {
  document.title = strings.addPlayerLink;

  const [name, setName] = useState("");
  const [guild, setGuild] = useState("");
  const [levelLand, setLevelLand] = useState("1");
  const [levelSea, setLevelSea] = useState("1");
  const [characterClass, setCharacterClass] = useState("noble");
  const [server, setServer] = useState("bergruen");


  const onSubmit = (event) => {
    event.preventDefault();

    const newPlayer = {
      name: name,
      guild: guild || null,
      level_land: parseInt(levelLand),
      level_sea: parseInt(levelSea),
      character_class: characterClass,
      server: server,
    };

    let res;
    addPlayer(server, newPlayer).then(fetchResponse => {
      res = fetchResponse;
      return fetchResponse.json();
    }).then(json => {
      if (!res.ok) {
        alert(json.msg);
      } else {
        props.history.push(`/players/${server}/${name}`);
      }
    })

  }

  return (
    <ContentWrapper>
      <form onSubmit={onSubmit}>
        <InputGroup>
          <label>{strings.name}</label>
          <TextInput value={name} onChange={e => setName(e.target.value)} />
        </InputGroup>

        <InputGroup>
          <label>{strings.server}</label>
          <Select value={server} onChange={e => setServer(e.target.value)} >
            <option value="bergruen">Bergruen</option>
            <option value="luxplena">LuxPlena</option>
          </Select>
        </InputGroup>

        <InputGroup>
          <label>{strings.class}</label>
          <Select value={characterClass} onChange={e => setCharacterClass(e.target.value)}>
            <option value="noble">Noble</option>
            <option value="magic_knight">Magic Knight</option>
            <option value="court_magician">Court Magician</option>

            <option value="saint">Saint</option>
            <option value="priest">Priest</option>
            <option value="shaman">Shaman</option>

            <option value="mercenary">Mercenary</option>
            <option value="guardian_swordsman">Guardian Swordsman</option>
            <option value="gladiator">Gladiator</option>

            <option value="explorer">Explorer</option>
            <option value="sniper">Sniper</option>
            <option value="excavator">Excavator</option>
          </Select>
        </InputGroup>

        <InputGroup>
          <label>{strings.guild}</label>
          <TextInput value={guild} onChange={e => setGuild(e.target.value)} />
        </InputGroup>

        <InputGroup>
          <label>{strings.levelLand}</label>
          <TextInput value={levelLand} onChange={e => setLevelLand(e.target.value)} />
        </InputGroup>

        <InputGroup>
          <label>{strings.levelSea}</label>
          <TextInput value={levelSea} onChange={e => setLevelSea(e.target.value)} />
        </InputGroup>

        <Button
          backgroundColorOnHover="#00cc6d"
          borderColorOnHover="green"
          padding="5px 15px"
          margin="0px 10px"
          type="submit"
        >
          {strings.addButton}
        </Button>
      </form>
    </ContentWrapper>
  )
}

export default PlayerAdd;