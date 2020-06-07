import React, { useState, useEffect } from "react";
import { getPlayers, createMatches } from "../../fetch";
import { ContentWrapper} from "../Layout/LayoutStyles";
import { NavbarExtension, FetchStateMessage } from "../Common/Common";
import { H2, ClassIcon, Button } from "../Common/CommonStyles";
import { getImagePath } from "../../helpers";
import {
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
} from "./CreateMatchesStyles";
import strings from "../../localization/strings";

const CreateMatches = (props) => {
  document.title = strings.createMatchesLink;

  const currentServer = props.match.params.server;
  const [players, setPlayers] = useState(null);
  const [loading, setLoading] = useState(true);

  const [searchString, setSearchString] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [addedPlayers, setAddedPlayers] = useState([]);

  const [keyword, setKeyword] = useState("");
  const [chatlog, setChatlog] = useState("");

  useEffect(() => {
    setLoading(true);
    setPlayers(null);
    setSearchResults([]);
    setAddedPlayers([]);

    let res;
    getPlayers(currentServer).then(fetchResponse => {
      res = fetchResponse;
      return fetchResponse.json()
    }).then(json => {
      if (!res.ok) {
        alert(json.msg)
      } else {
        setPlayers(json);
      }
      setLoading(false);
    });
  }, [currentServer])

  const onSearch = (event) => {
    setSearchString(event.target.value);
  
    if (event.target.value.length <= 1) {
      setSearchResults([]);
    } else {
      const matchingPlayers = players.filter(p => p.name.toLowerCase().includes(event.target.value.toLowerCase()));
      setSearchResults(matchingPlayers);
    }
  }

  const onSearchKeyUp = (event) => {
    if (event.keyCode === 13) { // enter
      event.preventDefault();
      addPlayer(searchResults[0] || null)
    }
  }

  const addPlayer = (player) => {
    if (!addedPlayers.includes(player) && player !== null) {
      setAddedPlayers([...addedPlayers, player]);
    }
    setSearchResults([]);
    setSearchString("");
  }

  const removePlayer = (player) => {
    setAddedPlayers(addedPlayers.filter(p => p !== player));
  }

  const parseChatlog = () => {
    const regex = new RegExp(`(\\w{1,13}):\\s(${keyword})$`, "i")

    const notFound = [];
    const playerObjects = [];

    chatlog.split("\n").forEach(line => {
      const match = line.trimRight().match(regex);
      if (match) {
        const playerName = match[1];
        const playerObj = players.filter(p => p.name === playerName)[0] || null;

        if (playerObj && !addedPlayers.includes(playerObj)) {
          playerObjects.push(playerObj);
        } else if (playerObj === null) {
          notFound.push(playerName);
        }
      }
    })

    setAddedPlayers([...addedPlayers, ...playerObjects]);
    if (notFound.length >= 1) {
      alert(strings.formatString(strings.notFound, {
        names: notFound.toString(),
      }))
    }
  }

  const startMatches = () => {
    const ids = [];
    addedPlayers.forEach(p => ids.push(p.id));

    if (window.confirm(strings.startMatchesConfirm)) {
      createMatches(currentServer, ids).then(res => {
        if (res.status === 201) {
          props.history.push(`/active_matches/${currentServer}`)
        } else if (res.status === 423) {
          alert(strings.alreadyActiveMatchesError)
        }
      })
    }
  }

  return (
    <>
      <NavbarExtension url="create_matches" currentServer={currentServer} />

      <ContentWrapper>
        <FetchStateMessage loading={loading} error={false}>
          <Grid>
            <SearchPlayerColumn>
              <H2>{strings.addPlayerHeader}</H2>
              <SearchInputWrapper>
                <SearchInput
                  type="text"
                  value={searchString}
                  onChange={onSearch}
                  onKeyUp={onSearchKeyUp}
                  placeholder={strings.searchPlayerPlaceholder}
                />
              </SearchInputWrapper>
              <SearchResults>
                {searchResults.sort((a, b) => a.name.length - b.name.length).map(player => {
                  return (
                    <PlayerWrapper onClick={() => addPlayer(player)}>
                      <ClassIcon
                        width={38}
                        marginRight={5}
                        src={getImagePath(`class_icons/male_${player.class.key}.png`)}
                      />
                      <span>{player.name}</span>
                    </PlayerWrapper>
                  )
                })}
              </SearchResults>
            </SearchPlayerColumn>

            <ChatlogPlayerColumn>
              <H2>{strings.addPlayerChatlogHeader}</H2>
              <ChatlogWrapper>
                <KeywordInput
                  placeholder={strings.keywordPlaceholder}
                  value={keyword}
                  onChange={e => setKeyword(e.target.value)}
                />
                <ChatlogTextArea
                  value={chatlog}
                  onChange={e => setChatlog(e.target.value)}
                />
                <Button
                  backgroundColorOnHover="lightblue"
                  borderColorOnHover="skyblue"
                  padding="5px 15px"
                  onClick={parseChatlog}
                >
                  {strings.parseButton}
                </Button>
              </ChatlogWrapper>
            </ChatlogPlayerColumn>

            <AddedPlayerColumn>
              <H2>{strings.players} ({addedPlayers.length})</H2>
              <AddedPlayerList>
                {addedPlayers.map(player => {
                    return (
                      <PlayerWrapper onClick={() => removePlayer(player)}>
                        <ClassIcon
                          width={38}
                          marginRight={5}
                          src={getImagePath(`class_icons/male_${player.class.key}.png`)}
                        />
                        <span>{player.name}</span>
                      </PlayerWrapper>
                    )
                  })}
              </AddedPlayerList>
            </AddedPlayerColumn>
          </Grid>
          <Button
            backgroundColorOnHover="#00cc6d"
            borderColorOnHover="green"
            padding="5px 15px"
            margin="20px 0px"
            width="100%"
            fontSize="18px"
            onClick={startMatches}
          >
            {strings.startMatchesButton}
          </Button>
        </FetchStateMessage>
      </ContentWrapper>
    </>
  )
}

export default CreateMatches;