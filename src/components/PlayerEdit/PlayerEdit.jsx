import React, { useState, useEffect } from "react";
import { getPlayer, updatePlayer } from "../../fetch";
import { ContentWrapper } from "../Layout/LayoutStyles";
import { FetchStateMessage } from "../Common/Common";
import { Button } from "../Common/CommonStyles";
import {
  InputGroup,
  TextInput,
  Select
} from "./PlayerEditStyles";
import strings from "../../localization/strings";

const PlayerEdit = (props) => {
  document.title = strings.playerEdit;

  const currentServer = props.match.params.server;
  const currentPlayerName = props.match.params.name;

  const [player, setPlayer] = useState(null);
  const [loading, setLoading] = useState(true);
  const [hasError, setHasError] = useState(false);

  const [levelLand, setLevelLand] = useState(null);
  const [levelSea, setLevelSea] = useState(null);
  const [characterClass, setCharacterClass] = useState(null);

  useEffect(() => {
    let res;
    getPlayer(currentServer, currentPlayerName).then(fetchResponse => {
      res = fetchResponse;
      return fetchResponse.json();
    }).then(json => {
      if (!res.ok) {
        setHasError(true);
        console.error(json.msg);
      } else {
        setPlayer(json);
        setLevelLand(json.level_land);
        setLevelSea(json.level_sea);
        setCharacterClass(json.class.key);
      }
      setLoading(false);
    })

  }, [currentServer, currentPlayerName])

  const onSubmit = (event) => {
    event.preventDefault();

    const newPlayer = {
      name: player.name,
      guild: player.guild,
      level_land: parseInt(levelLand),
      level_sea: parseInt(levelSea),
      character_class: characterClass,
      server: player.server.key,
      points: player.points,
      wins: player.wins,
      losses: player.losses,
      draws: player.draws,
    };

    let res;
    updatePlayer(currentServer, currentPlayerName, newPlayer).then(fetchResponse => {
      res = fetchResponse;
      return fetchResponse.json();
    }).then(json => {
      if (!res.ok) {
        alert(json.msg);
      } else {
        props.history.push(`/players/${currentServer}/${currentPlayerName}`);
      }
    })
  }

  return (
    <ContentWrapper>
      <FetchStateMessage loading={loading} error={hasError}>
        {player && (
          <form onSubmit={onSubmit}>
            <InputGroup>
              <label>{strings.name}</label>
              <TextInput disabled value={player.name} />
            </InputGroup>

            <InputGroup>
              <label>{strings.server}</label>
              <Select disabled value={player.server}>
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
              <TextInput disabled value={player.guild} />
            </InputGroup>

            <InputGroup>
              <label>{strings.levelLand}</label>
              <TextInput value={levelLand} onChange={e => setLevelLand(e.target.value)} />
            </InputGroup>

            <InputGroup>
              <label>{strings.levelSea}</label>
              <TextInput value={levelSea} onChange={e => setLevelSea(e.target.value)} />
            </InputGroup>

            <InputGroup>
              <label>{strings.points}</label>
              <TextInput disabled value={player.points} />
            </InputGroup>

            <InputGroup>
              <label>{strings.wins}</label>
              <TextInput disabled value={player.wins} />
            </InputGroup>

            <InputGroup>
              <label>{strings.losses}</label>
              <TextInput disabled value={player.losses} />
            </InputGroup>

            <InputGroup>
              <label>{strings.draws}</label>
              <TextInput disabled value={player.draws} />
            </InputGroup>

            <Button
              backgroundColorOnHover="#00cc6d"
              borderColorOnHover="green"
              padding="5px 15px"
              margin="0px 10px"
              type="submit"
            >
              {strings.saveButton}
            </Button>
          </form>
        )}
      </FetchStateMessage>
    </ContentWrapper>
  )
}

export default PlayerEdit;