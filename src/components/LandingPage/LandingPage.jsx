import React from "react";
import { ContentWrapper } from "../Layout/LayoutStyles";
import { H2, Text } from "../Common/CommonStyles";
import {
  Banner,
  Grid,
  GridItem,
} from "./LandingPageStyles";
import strings from "../../localization/strings";

const LandingPage = () => {
  document.title = strings.homepage;
  const startDate = new Date("July 12, 2020 00:00:00")

  return (
    <>
      <Banner />
      <ContentWrapper>
        <Grid>
          <GridItem row={1} start={1} end={3} rowS={1} startS={1} endS={2}>
            <H2>{strings.aboutHeader}</H2>
            <Text><p>{strings.formatString(strings.aboutText1, {date: startDate.toLocaleDateString()})}</p></Text>
            <Text>
              <span>{strings.aboutTextChange}</span><br />
              <span>{strings.aboutChange1}</span><br />
              <span>{strings.aboutChange2}</span><br />
              <span>{strings.aboutChange3}</span><br />
            </Text>
          </GridItem>

          <GridItem row={2} start={1} end={2} rowS={2} startS={1} endS={2}>
            <H2>{strings.rulesHeader}</H2>
            <Text>
              <ul>
                <li><b>1.</b> {strings.rule1}</li>
                <li><b>2.</b> {strings.rule2}</li>
                <li><b>3.</b> {strings.rule3}</li>
                <li><b>4.</b> {strings.rule4}</li>
                <li><b>5.</b> {strings.rule5}</li>
                <li><b>6.</b> {strings.rule6}</li>
                <li><b>7.</b> {strings.rule7}</li>
              </ul>
              <p>{strings.rulesInfoText}</p>
            </Text>
          </GridItem>

          <GridItem row={2} start={2} end={3} rowS={3} startS={1} endS={2}>
            <H2>{strings.participateHeader}</H2>
            <Text>
              <p>{strings.participateText1}</p>
              <p>{strings.participateText2}</p>
              <p>{strings.participateText3}</p>
              <p>{strings.participateText4}</p>
            </Text>
          </GridItem>

          <GridItem row={3} start={1} end={3} rowS={4} startS={1} endS={2}>
            <H2>{strings.prizesHeader}</H2>
            <Text>
              <p>{strings.prizesText1}</p>
              <ul>
                <li>{strings.prizesText2}</li>
                <li>{strings.prizesText3}</li>
              </ul>
            </Text>
          </GridItem>
        </Grid>
      </ContentWrapper>
    </>
  )
}

export default LandingPage;