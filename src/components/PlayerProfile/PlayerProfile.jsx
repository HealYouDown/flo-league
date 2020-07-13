import React, { useState, useEffect } from "react";
import { getPlayer, updateMatchWinner } from "../../fetch";
import { ContentWrapper } from "../Layout/LayoutStyles";
import { getImagePath } from "../../helpers";
import { FetchStateMessage } from "../Common/Common";
import { Flex, ClassIcon, RouterLink, CenteredSpan, H2, Button } from "../Common/CommonStyles";
import {
  Grid,
  PlayerInfoColumn,
  PlayerInfoTable,
  PlayerInfoName,
  MatchHistoryColumn,
  ResultSpan,
  TableRow,
  MatchHistoryTable
} from "./PlayerProfileStyles";
import { isLoggedIn } from "../../auth";
import strings from "../../localization/strings";

const PlayerProfile = (props) => {
  const currentServer = props.match.params.server;
  const name = props.match.params.name;

  const [player, setPlayer] = useState(null);
  const [loading, setLoading] = useState(true);
  const [hasError, setHasError] = useState(false);

  const [editId, setEditId] = useState(null);
  const [selectedWinner, setSelectedWinner] = useState(null);

  useEffect(() => {
    setLoading(true);
    setPlayer(null);

    let res;
    getPlayer(currentServer, name).then(fetchResponse => {
      res = fetchResponse;
      return fetchResponse.json()
    }).then(json => {
      if (!res.ok) {
        setHasError(true);
        console.error(json.msg)
      } else {
        setPlayer(json);
        document.title = strings.formatString(strings.playerProfile, {
          name: json.name,
        });
      }
      setLoading(false);
    });
  }, [currentServer, name])

  const enableMatchEdit = (match, opponent) => {
    // A match can be edited if it is the last one of each player
    // Check if its the last one of the current player profile
    const playerMatchIds = [];
    player.matches.forEach(m => playerMatchIds.push(m.id));
    const latestMatchId = Math.max(...playerMatchIds);

    if (match.id !== latestMatchId) {
      alert(strings.notLatestMatchError);
      return;
    }

    // get second player matches
    getPlayer(currentServer, opponent.name)
    .then(res => res.json())
    .then(json => {
      const opponentMatchIds = [];
      json.matches.forEach(m => opponentMatchIds.push(m.id));
      const opponentLatestMatchId = Math.max(...opponentMatchIds);

      if (opponentLatestMatchId === match.id) {
        setEditId(match.id);
        setSelectedWinner(match.winner.value.toString());
      } else {
        alert(strings.notLatestMatchError);
      }
    });
  }

  const onWinnerChange = (event) => {
    setSelectedWinner(event.target.value);
    const newWinner = parseInt(event.target.value);
  
    let res;
    updateMatchWinner(editId, newWinner).then(fetchResponse => {
      res = fetchResponse;
      return fetchResponse.json();
    }).then(json => {
      if (!res.ok) {
        alert(json.msg);
      } else {
        // update local list to reflect changes by server
        setPlayer(json.user)
        setEditId(null);
        setSelectedWinner(null);
      }
    })
  }

  return (
    <ContentWrapper>
      <FetchStateMessage loading={loading} error={hasError}>
        {player && (
          <Grid>
            <PlayerInfoColumn>
              <Flex flexFlow="row" alignItems="center">
                <ClassIcon
                  width={50}
                  marginRight={5}
                  src={getImagePath(`class_icons/male_${player.class.key}.png`)}
                />
                <PlayerInfoName>{player.name}</PlayerInfoName>
              </Flex>

              <PlayerInfoTable>
                <tbody>
                  <tr>
                    <td>{strings.server}</td>
                    <td>{player.server.value}</td>
                  </tr>
                  <tr>
                    <td>{strings.level}</td>
                    <td>{player.level_land} / {player.level_sea}</td>
                  </tr>
                  <tr>
                    <td>{strings.guild}</td>
                    <td>{player.guild || "/"}</td>
                  </tr>
                  <tr>
                    <td>{strings.points}</td>
                    <td>{player.points}</td>
                  </tr>
                  <tr>
                    <td>{strings.wins}</td>
                    <td>{player.wins}</td>
                  </tr>
                  <tr>
                    <td>{strings.losses}</td>
                    <td>{player.losses}</td>
                  </tr>
                  <tr>
                    <td>{strings.draws}</td>
                    <td>{player.draws}</td>
                  </tr>
                </tbody>
              </PlayerInfoTable>
            </PlayerInfoColumn>

            <MatchHistoryColumn>
              <H2>{strings.matchesHeader}</H2>
              {(player.matches.length >= 1)
              ? (
                <MatchHistoryTable>
                  <thead>
                    <tr>
                      <th>{strings.opponent}</th>
                      <th>{strings.result}</th>
                      <th>{strings.date}</th>
                      {isLoggedIn() && (
                        <th>{strings.edit}</th>
                      )}
                    </tr>
                  </thead>
                  <tbody>
                    {player.matches.sort((a, b) => b.id - a.id).map((match, index) => {
                      let opponent;
                      let playerKey;
                      if (match.player_1.name === player.name) {
                        opponent = match.player_2;
                        playerKey = "player_1";
                      } else {
                        opponent = match.player_1;
                        playerKey = "player_2";
                      }

                      let result;
                      let pointsChange = match[playerKey].points_change.toString();
                      let pointsOperator = (pointsChange > 0) ? "+" : "";

                      if (match.winner.value === 2) {
                        result = <span>{strings.draw} (<ResultSpan color="orange">{`${pointsOperator}${pointsChange}`}</ResultSpan>)</span>
                      } else if ((match.winner.value === 0 && playerKey === "player_1") || (match.winner.value === 1 && playerKey === "player_2")) {
                        result = <span>{strings.win} (<ResultSpan color="green">{`${pointsOperator}${pointsChange}`}</ResultSpan>)</span>
                      } else {
                        result = <span>{strings.loss} (<ResultSpan color="red">{`${pointsOperator}${pointsChange}`}</ResultSpan>)</span>
                      }

                      // edit is enabled for this match
                      if (editId === match.id) {
                        console.log(selectedWinner);
                        result = (
                          <select
                            value={selectedWinner}
                            onChange={onWinnerChange}
                          >
                            <option value="0">{match.player_1.name} {strings.win}</option>
                            <option value="1">{match.player_2.name} {strings.win}</option>
                            <option value="2">{strings.draw}</option>
                          </select>
                        )
                      }

                      const matchDate = new Date(match.date).toLocaleString();

                      return (
                        <TableRow even={index % 2}>
                          <td>
                            <Flex flexFlow="row" alignItems="center">
                              <ClassIcon
                                width={38}
                                marginRight={5}
                                src={getImagePath(`class_icons/male_${opponent.class.key}.png`)}
                              />
                              <RouterLink to={`/players/${match.server.key}/${opponent.name}`}>
                                {opponent.name} ({opponent.level_land}/{opponent.level_sea})
                              </RouterLink>
                            </Flex>
                          </td>
                          <td>{result}</td>
                          <td>{matchDate}</td>
                          {isLoggedIn() && (
                            <td>
                              <Button
                                backgroundColorOnHover="#00cc6d"
                                borderColorOnHover="green"
                                padding="3px 10px"
                                onClick={() => enableMatchEdit(match, opponent)}
                              >
                                {strings.edit}
                              </Button>
                            </td>
                          )}
                        </TableRow>
                      )
                    })}
                  </tbody>
                </MatchHistoryTable>
              )
              : (
                <CenteredSpan>{strings.noMatchesPlayed}</CenteredSpan>
              )}
            </MatchHistoryColumn>
          </Grid>
        )}
      </FetchStateMessage>
    </ContentWrapper>
  )
}

export default PlayerProfile;