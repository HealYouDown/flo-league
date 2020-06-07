import React, { useState, useEffect } from "react";
import { getActiveMatches, setActiveMatchWinner, deleteActiveMatches } from "../../fetch";
import { ContentWrapper} from "../Layout/LayoutStyles";
import { NavbarExtension, FetchStateMessage } from "../Common/Common";
import { calculateEloGain } from "../../helpers";
import { ClassIcon, RouterLink, CenteredSpan, Flex, Button } from "../Common/CommonStyles";
import { getImagePath } from "../../helpers";
import { isLoggedIn } from "../../auth";
import {
  Line,
  VersusWrapper,
  VersusText,
  PlayerSub,
  EloGain,
} from "./ActiveMatchesStyles";
import strings from "../../localization/strings";

const Player = ({player, p2_points}) => {
  return (
    <Flex
      flexFlow="column"
      alignItems="center"
      justifyContent="center"
    >
      <ClassIcon
        width={50}
        marginRight={0}
        src={getImagePath(`class_icons/male_${player.class.key}.png`)}
      />
      <RouterLink to={`/players/${player.server.key}/${player.name}`}>
        {player.name}
      </RouterLink>
      <Flex flexFlow="column" alignItems="center">
        <PlayerSub>
          {strings.points}: {player.points}
          <EloGain> (+{calculateEloGain(player.points, p2_points)})</EloGain>
        </PlayerSub>
        <PlayerSub>{strings.level}: {player.level_land} / {player.level_sea}</PlayerSub>
      </Flex>
    </Flex>
  )
}


const ActiveMatches = (props) => {
  document.title = strings.matchesLink;

  const currentServer = props.match.params.server;
  const [matches, setMatches] = useState(null);
  const [loading, setLoading] = useState(true);
  const [hasError, setHasError] = useState(false);

  useEffect(() => {
    setLoading(true);
    setMatches(null);

    let res;
    getActiveMatches(currentServer).then(fetchResponse => {
      res = fetchResponse;
      return fetchResponse.json()
    }).then(json => {
      if (!res.ok) {
        setHasError(true);
        console.error(json.msg)
      } else {
        setMatches(json);
      }
      setLoading(false);
    });
  }, [currentServer])

  const setWinner = (matchId, winner) => {
    /*
      0: Player 1
      1: Player 2
      2: Draw
    */
    let res;
    setActiveMatchWinner(currentServer, matchId, winner).then(fetchResponse => {
      res = fetchResponse;
      return fetchResponse.json()
    }).then(json => {
      if (!res.ok) {
        alert(json.msg)
      } else {
        // delete match from matches
        setMatches(matches.filter(m => m.id !== matchId))
      }
    });
  }

  const deleteAllMatches = () => {
    if (!window.confirm(strings.deleteMatchesConfirm1)) {
      return;
    }

    if (!window.confirm(strings.deleteMatchesConfirm2)) {
      return;
    }

    if (!window.confirm(strings.deleteMatchesConfirm3)) {
      return;
    }

    let res;
    deleteActiveMatches(currentServer).then(fetchResponse => {
      res = fetchResponse;
      return fetchResponse.json()
    }).then(json => {
      if (!res.ok) {
        alert(json.msg);
      } else {
        setMatches([]);
      }
    })
  }

  return (
    <>
      <NavbarExtension url="active_matches" currentServer={currentServer} />

      <ContentWrapper>
        <FetchStateMessage loading={loading} error={hasError}>
          {(matches && matches.length > 0) && (
            <Flex
              flexFlow="column"
              alignItems="center"
              justifyContent="center"
            >
              {isLoggedIn() && (
                <Button
                  padding="5px 15px"
                  backgroundColorOnHover="tomato"
                  broderColorOnHover="orangered"
                  margin="0px 0px 20px 0px"
                  onClick={deleteAllMatches}
                >
                  {strings.deleteMatchesButton}
                </Button>
              )}
              {matches.map((match, index) => {
                return (
                  <React.Fragment key={match.id}>
                    {index !== 0 && (
                      <Line />
                    )}
                    <Flex flexFlow="row" alignItems="center">
                      <Player player={match.player_1} p2_points={match.player_2.points} />
              
                      <VersusWrapper>
                        <VersusText>VS</VersusText>
                      </VersusWrapper>
              
                      <Player player={match.player_2} p2_points={match.player_1.points} />
                    </Flex>
                    {isLoggedIn() && (
                      <Flex flexFlow="row" justifyContent="space-evenly" alignItems="center">
                        <Button
                          backgroundColorOnHover="#00cc6d"
                          borderColorOnHover="green"
                          padding="5px 15px"
                          margin="0px 10px"
                          onClick={() => setWinner(match.id, 0)}
                        >
                          {match.player_1.name}
                        </Button>
                        <Button
                          backgroundColorOnHover="orange"
                          borderColorOnHover="darkorange"
                          padding="5px 15px"
                          margin="0px 10px"
                          onClick={() => setWinner(match.id, 2)}
                        >
                          {strings.draw}
                        </Button>
                        <Button
                          backgroundColorOnHover="#00cc6d"
                          borderColorOnHover="green"
                          padding="5px 15px"
                          margin="0px 10px"
                          onClick={() => setWinner(match.id, 1)}
                        >
                          {match.player_2.name}
                        </Button>
                      </Flex>
                    )}
                  </React.Fragment>
                )
              })}
            </Flex>
          )}
          {(matches && matches.length === 0) && (
            <CenteredSpan>{strings.noMatchesFound}</CenteredSpan>
          )}
        </FetchStateMessage>
      </ContentWrapper>
    </>
  )
}

export default ActiveMatches;
