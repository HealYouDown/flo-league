import React, { useState, useEffect } from "react";
import { getRanking } from "../../fetch";
import { ContentWrapper } from "../Layout/LayoutStyles";
import { NavbarExtension, FetchStateMessage} from "../Common/Common";
import { getImagePath } from "../../helpers";
import { ClassIcon, RouterLink, CenteredSpan, Flex } from "../Common/CommonStyles";
import {
  TableWrapper,
  Table,
  TableHeader,
  TableData,
  TableRow,
} from "./RankingStyles";
import strings from "../../localization/strings";

const Ranking = (props) => {
  document.title = strings.rankingLink;
  const currentServer = props.match.params.server;
  const [players, setPlayers] = useState(null);
  const [loading, setLoading] = useState(true);
  const [hasError, setHasError] = useState(false);

  useEffect(() => {
    setLoading(true);
    setPlayers(null);
    let res;
    getRanking(currentServer).then(fetchResponse => {
      res = fetchResponse;
      return fetchResponse.json()
    }).then(json => {
      if (!res.ok) {
        setHasError(true);
        console.error(json.msg)
      } else {
        setPlayers(json);
      }
      setLoading(false);
    });
  }, [currentServer])

  return (
    <>
      <NavbarExtension url="ranking" currentServer={currentServer} />

      <ContentWrapper>
        <FetchStateMessage loading={loading} error={hasError}>
          {(players && players.length > 0) && (
            <TableWrapper>
              <Table>
                <thead>
                  <tr>
                    <TableHeader align="center">{strings.rank}</TableHeader>
                    <TableHeader align="center">{strings.points}</TableHeader>
                    <TableHeader align="left">{strings.name}</TableHeader>
                    <TableHeader align="center">{strings.level}</TableHeader>
                    <TableHeader align="center">{strings.winsLossesDraws}</TableHeader>
                  </tr>
                </thead>
                <tbody>
                  {players.sort((a, b) => b.points - a.points).map((player, index) => {
                    let rank = index + 1;
                    let rankColor;
                    switch (rank) {
                      case 1:
                        rankColor = "#FFD700";
                        break;
                      case 2:
                        rankColor = "#C0C0C0";
                        break;
                      case 3:
                        rankColor = "#cd7f32";
                        break;
                      default:
                        rankColor = "#708090"; 
                    }

                    // Firefox needs y to be 30, chrome 25.
                    // InstallTrigger is Firefox API for addons
                    const y = typeof InstallTrigger !== 'undefined' ? "30" : "25";

                    return (
                      <TableRow key={player.name} even={index % 2}>
                        <TableData align="center">
                          <svg width={50} height={50}>
                            <path d="M25,0 L50,25 L25,50 L0,25 L25,0 Z" fill={rankColor} />
                            <text textAnchor="middle" alignmentBaseline="central" x="25" y={y} fill="white">{rank}</text>
                          </svg>
                        </TableData>
                        <TableData align="center">{player.points}</TableData>
                        <TableData align="left">
                          <Flex flexFlow="row" alignItems="center" >
                            <ClassIcon
                              width={38}
                              marginRight={5}
                              src={getImagePath(`class_icons/male_${player.class.key}.png`)}
                            />
                            <RouterLink
                              to={`/players/${player.server.key}/${player.name}`}
                            >
                              {player.name}
                            </RouterLink>
                          </Flex>
                        </TableData>
                        <TableData align="center">{player.level_land} / {player.level_sea}</TableData>
                        <TableData align="center">{player.wins} : {player.losses} : {player.draws}</TableData>
                      </TableRow>
                    )
                  })}
                </tbody>
              </Table>
            </TableWrapper>
          )}
          {(players && players.length === 0) && (
            <CenteredSpan>{strings.noPlayersFound}</CenteredSpan>
          )}
        </FetchStateMessage>
      </ContentWrapper>
    </>
  )
}

export default Ranking;